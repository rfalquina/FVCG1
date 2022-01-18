def koppen(temp,precip, lat):
    "This function computes the Koppen climate type for a given cell"
    #    The koppen climate type is computed
    #    based on 12 months daily average temperature
    #    and 12 months monthly average precipitation
    #    
    #    temp is a 12 values vector, celsius 
    #    precip is a 12 values vector, milimeters
    #    lat is the latitude, degrees
    if lat < 0.0:
        tmp1=temp[0:3] # jan, feb, mar
        tmp2=temp[3:6] # apr, may, jun
        tmp3=temp[6:9] # jul, aug, sep
        tmp4=temp[9:12] # oct, nov, dec
        prec1=precip[0:3]
        prec2=precip[3:6]
        prec3=precip[6:9]
        prec4=precip[9:12]
        temp[6:9]=tmp1
        temp[9:12]=tmp2
        temp[0:3]=tmp3
        temp[3:6]=tmp4
        precip[6:9]=prec1
        precip[9:12]=prec2
        precip[0:3]=prec3
        precip[3:6]=prec4


    climate = np.dtype('S3')

    # Group E (Polar and alpine)
    if max(temp) < 10.0:
        # Tundra (ET)
        if max(temp) > 0.0:
            climate = 'ET'
        # Ice cap (EF)
        else:
            climate = 'EF'
        return climate
       
    # Group B (Arid and Semiarid)
#    if sum(precip) > 0.0:
    totalprecip = sum(precip)
#    else:
#        totalprecip = 0.000000001

    aridity = np.mean(temp) * 2.0

    warmprecip = sum(precip[3:9])

    # coolprecip = sum(precip[0:3]) + sum(precip[9:12])
    if warmprecip >= 0.6666*totalprecip:
        aridity = aridity + 28.0
    elif warmprecip >= 0.3334*totalprecip and warmprecip < 0.6666*totalprecip:
        aridity = aridity + 14.0
    else:
        aridity = aridity + 0.0

    # Arid Desert (BW)
    if totalprecip <= 5.0*aridity:
        # Hot Desert (BWh)
        if np.mean(temp) >= 18.0:
            climate = 'BWh'
        # Cold Desert (BWk)
        else:
            climate = 'BWk'
        return climate

    # Semi-Arid/Steppe (BS)
    elif totalprecip > 5.0*aridity and totalprecip < 10.0*aridity:
        # Hot Semi-Arid (BSh)
        if np.mean(temp) >= 18.0:
            climate = 'BSh'
        # Cold Semi-Arid (BSk)
        else:
            climate = 'BSk'
        return climate

    # Group A (Tropical)
    if min(temp) >= 18.0:
        # Tropical Rainforest
        if min(precip) >= 60.0:
            climate = 'Af'
        # Tropical Monsoon
        elif min(precip) < 60.0 and totalprecip >= 25.0*(100-min(precip)):
            climate = 'Am'
        else:
            # Tropical Savanna Dry Summer
            if np.where(precip==min(precip))[0][0] >= 3 and np.where(precip==min(precip))[0][0] <= 8:
                climate = 'As'
            # Tropical Savanna Dry Winter
            else:
                climate = 'Aw'
        return climate


    tempaboveten = np.shape(np.where(temp>10.0))[1] # months with T>10

    # The summer months are April through September (AMJJAS) on the Northern Hemisphere 
    # and the winter months are October through March (ONDJFM), and vice versa for the Southern Hemisphere

    psmin=min(precip[3:9]) # summer minimum precipitation
    pwmin=min(min(precip[0:3]),min(precip[9:12])) # winter minimum precipitation
    psmax=max(precip[3:9]) # summer maximum precipitation
    pwmax=max(max(precip[0:3]),max(precip[9:12])) # winter maximum precipitation

    # Group C (Temperate)

    if min(temp) > -3.0 and min(temp) < 18.0 and max(temp) >= 10.0:

        # Humid Subtropical (Cfa)
        if max(temp) >= 22.0:
            climate = 'Cfa'
        # Temperate Oceanic (Cfb)
        elif max(temp) < 22.0 and tempaboveten >= 4.0:
            climate = 'Cfb'
        # Subpolar Oceanic (Cfc)
        elif max(temp) < 22.0 and tempaboveten < 4.0:
            climate = 'Cfc'

        # Hot summer Mediterranean (Csa)
        if psmin < pwmin and pwmax > 3.0*psmin and psmin < 40.0 and \
            max(temp) >= 22.0:
            climate = 'Csa'
        # Warm summer Mediterranean (Csb)
        elif psmin < pwmin and pwmax > 3.0*psmin and psmin < 40.0  and \
            max(temp) < 22.0 and tempaboveten >= 4:
            climate = 'Csb'
        # Cool summer Mediterranean (Csc)
        elif psmin < pwmin and pwmax > 3.0*psmin and psmin < 40.0  and \
            max(temp) < 22.0 and tempaboveten < 4:
            climate = 'Csc'

        # Monsoon-influenced humid subtropical (Cwa)
        if pwmin < psmin and psmax > 10.0*pwmin and \
            max(temp) >= 22.0:
            climate = 'Cwa'
        # Subtropical Highland/Temperate Oceanic with Dry Winter (Cwb)
        elif pwmin < psmin and psmax > 10.0*pwmin and \
            max(temp) < 22.0 and tempaboveten >= 4:
            climate = 'Cwb'
        # Cold Subtropical Highland/Subpolar Oceanic with Dry Winter (Cwc)
        elif pwmin < psmin and psmax > 10.0*pwmin and \
            max(temp) < 22.0 and tempaboveten < 4:
            climate = 'Cwc'

        return climate

    # Group D (Continental)
    if min(temp) <= -3.0 and max(temp) >= 10.0:
        # Hot summer humid continental (Dfa)
        if max(temp) >= 22.0 :
            climate = 'Dfa'
        # Warm summer humid continental (Dfb)
        elif max(temp) < 22.0 and tempaboveten >= 4:
            climate = 'Dfb'
        # Subarctic (Dfc)
        elif max(temp) < 22.0 and tempaboveten < 4 and min(temp) > -38.0:
            climate = 'Dfc'
        # Extremely cold subarctic (Dfd)
        elif max(temp) < 22.0 and tempaboveten < 4 and min(temp) <= -38.0:
            climate = 'Dfd'

        # Hot, dry continental (Dsa)
        if psmin < pwmin and pwmax > 3.0*psmin and psmin < 40.0 and \
            max(temp) >= 22.0:
            climate = 'Dsa'
        # Warm, dry continental (Dsb)
        elif psmin < pwmin and pwmax > 3.0*psmin and psmin < 40.0 and \
            max(temp) < 22.0 and tempaboveten >= 4:
            climate = 'Dsb'
        # Dry, subarctic (Dsc)
        elif psmin < pwmin and pwmax > 3.0*psmin and psmin < 40.0 and \
            max(temp) < 22.0 and tempaboveten < 4 and min(temp) > -38.0:
            climate = 'Dsc'
        # Extremely cold, dry subarctic (Dsd)
        elif psmin < pwmin and pwmax > 3.0*psmin and psmin < 40.0 and \
            max(temp) < 22.0 and tempaboveten < 4 and min(temp) <= -38.0:
            climate = 'Dsd'

        # Monsoon-influenced hot humid continental (Dwa)
        if pwmin < psmin and psmax > 10.0*pwmin and \
            max(temp) >= 22.0:
            climate = 'Dwa'
        # Monsoon-influenced warm humid continental (Dwb)
        elif pwmin < psmin and psmax > 10.0*pwmin and \
            max(temp) < 22.0 and tempaboveten >= 4:
            climate = 'Dwb'
        # Monsoon-influenced subarctic (Dwc)
        elif pwmin < psmin and psmax > 10.0*pwmin and \
            max(temp) < 22.0 and tempaboveten < 4 and min(temp) > -38.0:
            climate = 'Dwc'
        # Monsoon-influenced extremely cold subarctic (Dwd)
        elif pwmin < psmin and psmax > 10.0*pwmin and \
            max(temp) < 22.0 and tempaboveten < 4 and min(temp) <= -38.0:
            climate = 'Dwd'

        return climate
