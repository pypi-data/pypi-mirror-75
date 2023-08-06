import copy

# generates the color_scale that can be used in graphs
def colors_scale(labels: list = []):
    # colors used in ZS
    zs_theme_colors = ["rgba(0, 98, 155, 1)", "rgba(1, 166, 220, 1)", "rgba(110, 43, 98, 1)", "rgba(134, 200, 188, 1)",
                       "rgba(160, 175, 198, 1)", "rgba(163, 178, 170, 1)", "rgba(182, 232, 128, 1)",
                       "rgba(184, 204, 123, 1)", "rgba(254, 203, 82, 1)", "rgba(255, 151, 255, 1)"]

    # checks for the length of labels
    # returns the colors from zs_theme_colors if the lables are less than or equals to the colors provided
    if len(labels) <= len(zs_theme_colors):
        return zs_theme_colors[:len(labels)]

    # returns the label number of colors by manupulating the zs_theme_colors
    elif len(labels) > len(zs_theme_colors):
        colors_scale = copy.deepcopy(zs_theme_colors)

        # checks whether the number of labels are exact multiples of number of zs_theme_colors
        # returns the manupulated colors from zs_theme_colors
        # condition for number of labels are not exactly the multiples of number of zs_theme_colors
        if (len(labels) / len(zs_theme_colors)) % 1 > 0:
            # increases the zs_theme_colors to the number of labels
            for num in range(int(len(labels) / len(zs_theme_colors))):
                # reduces the alpha in rgba of each color present in zs_theme_colors
                for color in range(len(zs_theme_colors)):
                    colors_scale.append(zs_theme_colors[color].replace(" 1)", (" " + str(
                        round(1 - (0.5 / int(len(labels) / len(zs_theme_colors))) * (num + 1), 3)) + ")")))
            return colors_scale[:len(labels)]

        # condition for number labels are exactly the multiples of number of zs_theme_colors
        elif (len(labels) / len(zs_theme_colors)) % 1 == 0:
            # increases the zs_theme_colors to the number of labels
            for num in range(int(len(labels) / len(zs_theme_colors)) - 1):
                # reduces the alpha in rgba of each color present in zs_theme_colors
                for color in range(len(zs_theme_colors)):
                    colors_scale.append(zs_theme_colors[color].replace(" 1)", (" " + str(
                        round(1 - (0.5 / (int(len(labels) / len(zs_theme_colors)) - 1)) * (num + 1), 3)) + ")")))
            return colors_scale[:len(labels)]

def discrete_colorscale(bvals, colors):
    """
    bvals - list of values bounding intervals/ranges of interest
    colors - list of rgb or hex colorcodes for values in [bvals[k], bvals[k+1]],0<=k < len(bvals)-1
    returns the plotly  discrete colorscale
    """
    if len(bvals) > len(colors):
        raise ValueError('len(boundary values) should be less than or equal to  len(colors)')
    bvals = sorted(bvals)     
    nvals = [(v-bvals[0])/(bvals[-1]-bvals[0]) for v in bvals]  #normalized values

    dcolorscale = [] #discrete colorscale
    for k in range(len(bvals)):
        dcolorscale.extend([[nvals[k], colors[k]]])
    return dcolorscale 