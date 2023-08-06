'''Perform THR computation on IVT data

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2020-07-22 09:58:36.
'''

from __future__ import print_function
import os
import numpy as np
from skimage import morphology
from ipart.utils import funcs
#import recon

def THR(ivtNV, kernel, oroNV=None, high_terrain=600, verbose=True):
    '''Perform THR filtering process on 3d data

    Args:
        ivtNV (NCVAR): 3D or 4D input IVT data, with dimensions
            (time, lat, lon) or (time, level, lat, lon).
        kernel (list or tuple): list/tuple of integers specifying the shape of
            the kernel/structuring element used in the gray erosion process.

    Keyword Args:
        oroNV (NCVAR or None): 2D array, surface orographic data in meters.
            This optional surface height info is used to perform a separate
            reconstruction computation for areas with high elevations, and
            the results can be used to enhance the continent-penetration
            ability of landfalling ARs. Sensitivity in landfalling ARs is
            enhanced, other areas are not affected. Needs to have compatible
            (lat, lon) shape as <ivt>.
            If None, omit this process and treat areas with different heights
            all equally.

            New in v2.0.
        high_terrain (float): minimum orographic height (in m) to define as high
            terrain area, within which a separate reconstruction is performed.
            Only used if <oroNV> is not None.

            New in v2.0.
        verbose (bool): print some messages or not.

    Returns:
        ivtNV (NCVAR): 3D or 4D array, input <ivt>.
        ivtrecNV (NCVAR): 3D or 4D array, the reconstruction component from the
            THR process.
        ivtanoNV (NCVAR): 3D or 4D array, the difference between input <ivt>
            and <ivtrecNV>.
    '''

    ivt=ivtNV.data
    ndim=np.ndim(ivt)
    ivt=np.squeeze(ivt)

    #-------------------3d ellipsoid-------------------
    ele=funcs.get3DEllipse(*kernel)

    #################### use a cube to speed up ##############
    # empirical
    if kernel[0]>=16 or kernel[1]>=6:
        ele=np.ones(ele.shape)
    ##########################################################

    # reconstruction element: a 6-connectivity element
    rec_ele=np.zeros([3,3,3])
    rec_ele[0,1,1]=1
    rec_ele[1,:,1]=1
    rec_ele[1,1,:]=1
    rec_ele[2,1,1]=1

    if verbose:
        print('\n# <THR>: Computing erosion ...')

    lm=morphology.erosion(ivt, selem=ele)

    if verbose:
        print('\n# <THR>: Computing reconstruction ...')

    ivtrec=morphology.reconstruction(lm, ivt, method='dilation', selem=rec_ele)

    # perform an extra reconstruction over land
    if oroNV is not None:
        orodata=np.squeeze(oroNV.data)
        oro_rs=np.where(orodata>=high_terrain, 1, 0)
        oro_rs=oro_rs[None,...]
        oro_rs=np.repeat(oro_rs, len(ivt), axis=0)

        ivtrec_oro=morphology.reconstruction(lm*oro_rs, ivt, method='dilation',
                selem=rec_ele)
        ivtano=np.ma.maximum(ivt-ivtrec, (ivt-ivtrec_oro)*oro_rs)
    else:
        ivtano=ivt-ivtrec

    ivtrec=ivt-ivtano

    axislist=ivtNV.axislist

    #---------If inputs are 4d, also return 4d---------
    if ndim==4:
        ivt=ivt[:,None,...]
        ivtrec=ivtrec[:,None,...]
        ivtano=ivtano[:,None,...]

    ivtrecNV=funcs.NCVAR(ivtrec, 'ivt_rec', axislist, {'name': 'ivt_rec',
        'long_name': '%s, THR reconstruction' %(getattr(ivt, 'long_name', '')),
        'standard_name': '%s, THR reconstruction' %(getattr(ivt, 'long_name', '')),
        'units': getattr(ivt, 'units', '')})

    ivtanoNV=funcs.NCVAR(ivtano, 'ivt_ano', axislist, {'name': 'ivt_ano',
        'long_name': '%s, THR anomaly' %(getattr(ivt, 'long_name', '')),
        'standard_name': '%s, THR anomaly' %(getattr(ivt, 'long_name', '')),
        'units': getattr(ivt, 'units', '')})

    return ivtNV, ivtrecNV, ivtanoNV

def rotatingTHR(filelist, varin, kernel, outputdir, oroNV=None,
        selector=None, high_terrain=600, verbose=True):
    '''Compute time filtering on data in different files.

    Args:
        filelist (list): list of abs paths to data files. User is responsible to
                    make sure files in list have correct chronological order.
                    Note that time axis in data files should be the 1st axis.
        varin (str): variable id in files.
        kernel (list or tuple): list/tuple of integers specifying the shape of
            the kernel/structuring element used in the gray erosion process.
        selector (utils.funcs.Selector): selector obj to select subset of data.
        outputdir (str): path to folder to save outputs.

    Keyword Args:
        oroNV (NCVAR): 2D array, surface orographic data in meters.
            This additional surface height info is used to perform a separate
            reconstruction computation for areas with high elevations, and
            the results can be used to enhance the continent-penetration
            ability of landfalling ARs. Sensitivity in landfalling ARs is
            enhanced, other areas are not affected. Needs to have compatible
            shape as <ivt>.
            If None, omit this process and treat areas with different heights
            all equally.

            New in v2.0.
        high_terrain (float): minimum orographic height to define as high
            terrain area, within which a separate reconstruction is performed.
            Only used if <oroNV> is not None.

            New in v2.0.
        verbose (bool): print some messages or not.

    Designed to perform temporal filtering on data that are too large to fit
    into memory, e.g. high-resolution data across multiple decades.

    Function will read in 2 files at once, call the filtering function on the
    concatenated data, and shift 1 step to the next 2 files. If at the begining,
    pad 0s to the left end. If in the mid, pad filtered data in the mid of
    the concatenated data in the previous step. If at the end, pad 0s to
    the right end.

    The filtering function <func> is assumed to apply a filtering window with
    odd length n, and truncates (n-1)/2 points from both ends. If the function
    doesn't truncate data, will raise an exception.
    '''

    #----------------Check input files----------------
    funcs.checkFiles(filelist)

    for ii, fii in enumerate(filelist[:-1]):
        if ii==0:
            var1=funcs.readNC(fii, varin)
            var1=var1(selector)
        else:
            var1=var2
            del var2

        fii2=filelist[ii+1]
        var2=funcs.readNC(fii2, varin)
        var2=var2(selector)

        timeidx=funcs.interpretAxis('time',var1)
        if timeidx!=0:
            raise Exception("Time axis in variable is not at axis 0.")
        timeidx=funcs.interpretAxis('time',var2)
        if timeidx!=0:
            raise Exception("Time axis in variable is not at axis 0.")

        n1=var1.shape[0]

        vartmp=funcs.cat(var1,var2,axis=0)
        vartmp, vartmp_rec, vartmp_ano=THR(vartmp, kernel, oroNV=oroNV,
            high_terrain=high_terrain)

        # crop end points
        dt=kernel[0]
        vartmp_rec=vartmp_rec.sliceIndex(dt, -dt)
        vartmp_ano=vartmp_ano.sliceIndex(dt, -dt)

        if dt<=0:
            raise Exception("dt<=0 not supported yet")

        if verbose:
            print('\n# <rotatingTHR>: Concatenated var shape:',vartmp.shape)
            print('# <rotatingTHR>: Filtered var shape:',vartmp_rec.shape)
            print('# <rotatingTHR>: Length difference:',dt)

        if ii==0:
            #----------------------Pad 0s----------------------
            left_rec=var1.sliceIndex(0, dt)
            left_rec.data=left_rec.data*0
            left_rec.data.mask=True
            left_ano=var1.sliceIndex(0, dt)
            left_ano.data=left_ano.data*0
            left_ano.data.mask=True
        else:
            left_rec=mid_left_rec
            left_ano=mid_left_ano

        rec_pad=funcs.cat(left_rec,vartmp_rec,axis=0)
        rec1=rec_pad.sliceIndex(0, n1)

        ano_pad=funcs.cat(left_ano,vartmp_ano,axis=0)
        ano1=ano_pad.sliceIndex(0, n1)

        var1=vartmp.sliceIndex(0, n1)

        if verbose:
            print('\n# <rotatingTHR>: Shape of left section after padding:',
                    rec1.shape)

        rec1.id=vartmp_rec.id
        attdict={'long_name':'%s, THR reconstruction'\
                %(getattr(var1, 'long_name', ''))}
        attdict['standard_name']=attdict['long_name']
        attdict['title']=attdict['long_name']
        attdict['units']=var1.units
        rec1.attributes=attdict

        ano1.id=vartmp_ano.id
        attdict={'long_name':'%s, THR anomaly'\
                %(getattr(var1, 'long_name', ''))}
        attdict['standard_name']=attdict['long_name']
        attdict['title']=attdict['long_name']
        attdict['units']=var1.units
        ano1.attributes=attdict

        # left to pad in next iteration
        mid_left_rec=vartmp_rec.sliceIndex(n1-dt, n1)
        mid_left_ano=vartmp_ano.sliceIndex(n1-dt, n1)

        #-----------------------Save-----------------------
        fname=os.path.split(fii)[1]
        file_out_name='%s-THR-kernel-t%d-s%d.nc'\
                %(os.path.splitext(fname)[0], kernel[0], kernel[1])

        abpath_out=os.path.join(outputdir,file_out_name)
        print('\n### <testrotatingfilter>: Saving output to:\n',abpath_out)
        funcs.saveNC(abpath_out, var1, 'w')
        funcs.saveNC(abpath_out, rec1, 'a')
        funcs.saveNC(abpath_out, ano1, 'a')

        # save the right section for the last file
        if ii==len(filelist)-2:
            right=var2.sliceIndex(-dt, None)
            right.data=right.data*0
            right.data.mask=True
            rec2=rec_pad.sliceIndex(n1, None)
            rec2=funcs.cat(rec2,right,axis=0)

            ano2=ano_pad.sliceIndex(n1, None)
            ano2=funcs.cat(ano2,right,axis=0)

            var2=vartmp.sliceIndex(n1, None)

            if verbose:
                print('\n# <rotatingTHR>: Shape of last section after padding:', ano2.shape)

            rec2.id=vartmp_rec.id
            attdict={'long_name':'%s, THR reconstruction'\
                    %(getattr(var1, 'long_name', ''))}
            attdict['standard_name']=attdict['long_name']
            attdict['title']=attdict['long_name']
            attdict['units']=var2.units
            rec2.attributes=attdict

            ano2.id=vartmp_ano.id
            attdict={'long_name':'%s, THR anomaly'\
                    %(getattr(var1, 'long_name', ''))}
            attdict['standard_name']=attdict['long_name']
            attdict['title']=attdict['long_name']
            attdict['units']=var2.units
            ano2.attributes=attdict

            #-----------------------Save-----------------------
            fname=os.path.split(fii2)[1]
            file_out_name='%s-THR-kernel-t%d-s%d.nc'\
                    %(os.path.splitext(fname)[0], kernel[0], kernel[1])
            abpath_out=os.path.join(outputdir,file_out_name)
            print('\n### <testrotatingfilter>: Saving output to:\n',abpath_out)
            funcs.saveNC(abpath_out, var2, 'w')
            funcs.saveNC(abpath_out, rec2, 'a')
            funcs.saveNC(abpath_out, ano2, 'a')


    return

"""
def THRCyclicLongitude(ivt, kernel, oro=None, high_terrain=600, verbose=True):
    '''Perform THR filtering process on 3d data

    Args:
        ivt (TransientVariable): 3D or 4D input IVT data, with dimensions
            (time, lat, lon) or (time, level, lat, lon).
        kernel (list or tuple): list/tuple of integers specifying the shape of
            the kernel/structuring element used in the gray erosion process.

    Keyword Args:
        oro (TransientVariable): 2D array, surface orographic data in meters.
            This optional surface height info is used to perform a separate
            reconstruction computation for areas with high elevations, and
            the results can be used to enhance the continent-penetration
            ability of landfalling ARs. Sensitivity in landfalling ARs is
            enhanced, other areas are not affected. Needs to have compatible
            (lat, lon) shape as <ivt>.

            New in v2.0.
        high_terrain (float): minimum orographic height (in m) to define as high
            terrain area, within which a separate reconstruction is performed.
            Only used if <oro> is not None.

            New in v2.0.

    Returns:
        ivt (TransientVariable): 3D or 4D array, input <ivt>.
        ivtrec (TransientVariable): 3D or 4D array, the reconstruction
            component from the THR process.
        ivtano (TransientVariable): 3D or 4D array, the difference between
            input <ivt> and <ivtrec>.

    NOTE: only minor difference from non-zonally cyclic version. Not worth it.
    '''

    ndim=np.ndim(ivt)
    ivt=ivt(squeeze=1)

    #-------------------3d ellipsoid-------------------
    ele=funcs.get3DEllipse(*kernel)

    #################### use a cube to speed up ##############
    # empirical
    if kernel[0]>=16 or kernel[1]>=6:
        ele=np.ones(ele.shape)
    ##########################################################

    # reconstruction element: a 6-connectivity element
    rec_ele=np.zeros([3,3,3])
    rec_ele[0,1,1]=1
    rec_ele[1,:,1]=1
    rec_ele[1,1,:]=1
    rec_ele[2,1,1]=1

    if verbose:
        print('\n# <THR>: Computing erosion ...')

    lm=morphology.erosion(ivt.data, selem=ele)

    if verbose:
        print('\n# <THR>: Computing reconstruction ...')

    ivtrec=recon.reconstruction(lm, ivt, method='dilation', selem=rec_ele)

    # perform an extra reconstruction over land
    if oro is not None:
        oro_rs=MV.where(oro>=high_terrain, 1, 0)
        oro_rs=funcs.addExtraAxis(oro_rs,axis=0)
        oro_rs=np.repeat(oro_rs, len(ivt), axis=0)

        ivtrec_oro=recon.reconstruction(lm*oro_rs, ivt, method='dilation',
                selem=rec_ele)
        ivtano=MV.maximum(ivt-ivtrec, (ivt-ivtrec_oro)*oro_rs)
    else:
        ivtano=ivt-ivtrec

    ivtrec=ivt-ivtano

    if ndim==4:
        levax=cdms.createAxis([0,])
        levax.designateLevel()
        levax.id='z'
        levax.name='level'
        levax.units=''

        ivt=funcs.addExtraAxis(ivt,levax,1)
        ivtrec=funcs.addExtraAxis(ivtrec,levax,1)
        ivtano=funcs.addExtraAxis(ivtano,levax,1)

    axislist=ivt.getAxisList()
    ivtrec.setAxisList(axislist)
    ivtano.setAxisList(axislist)

    ivtrec.id='ivt_rec'
    ivtrec.long_name='%s, THR reconstruction' %(getattr(ivt, 'long_name', ''))
    ivtrec.standard_name=ivtrec.long_name
    ivtrec.title=ivtrec.long_name
    ivtrec.units=ivt.units

    ivtano.id='ivt_ano'
    ivtano.long_name='%s, THR anomaly' %(getattr(ivt, 'long_name', ''))
    ivtano.standard_name=ivtano.long_name
    ivtano.title=ivtano.long_name
    ivtano.units=ivt.units

    return ivt, ivtrec, ivtano
"""


