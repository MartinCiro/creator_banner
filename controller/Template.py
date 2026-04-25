# controller/Template.py
from html import escape

class Template:
    def __init__(self, config):
        self.config = config

    def _safe(self, value: str) -> str:
        return escape(value or "")

    def _branch_svg_url(self, primary: str, opacity: float = 1.0, rotate: bool = False) -> str:

        """Retorna el SVG de la rama con el color primario aplicado dinámicamente."""
        import urllib.parse, re
        rotate_attr = f"transform='rotate(180, 46, 35)'" if rotate else ""
        paths = """<path
       id="path101063"
       style="color:#000000;fill:#100c09;stroke-width:1.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 4.6017863,14.777393 c -1.2247504,-0.0052 -2.3660128,0.03236 -3.3067749,0.136425 -0.75260969,0.08325 -1.37743861,0.207215 -1.82056072,0.392741 -0.22156105,0.09276 -0.3988607,0.200849 -0.52348228,0.33383 -0.1240004,0.132318 -0.1899088,0.295075 -0.1813843,0.470772 -0.055626,2.636532 1.09079373,4.996581 2.7791586,6.888985 1.6897276,1.893932 3.9193337,3.325167 6.043042,4.114995 0.00256,7.92e-4 0.00514,0.0015 0.00775,0.0021 4.1461223,1.237221 8.8348623,0.426452 12.6307543,0.484208 0.0032,4.9e-5 0.0066,-5e-5 0.0098,0 3.463736,0.120564 6.176642,-0.05294 9.40046,0.349849 l -0.0057,-0.0021 c 0.847991,0.152259 1.977678,0.372698 2.710945,0.220659 0.183317,-0.03801 0.343859,-0.100144 0.468706,-0.201022 0.124847,-0.100877 0.210551,-0.244083 0.232543,-0.418062 0.04398,-0.347958 -0.135929,-0.805047 -0.592211,-1.447457 -0.003,-0.004 -0.0063,-0.0078 -0.0098,-0.01137 -3.171423,-3.322304 -7.028741,-6.153719 -11.085628,-8.511625 l -0.0062,-0.0041 C 19.023021,16.364557 16.920488,15.541435 14.689528,15.357235 14.1607,15.313455 13.456852,15.253394 12.640557,15.187736 11.007967,15.056422 8.9230704,14.905286 6.870883,14.828068 6.1013128,14.799108 5.3366212,14.780548 4.6017709,14.777428 Z m -0.00155,0.198954 c 0.7322729,0.0032 1.4951147,0.02175 2.262911,0.05064 v 5.17e-4 c 2.0474567,0.07704 4.1306527,0.227942 5.7619217,0.359151 0.815635,0.0656 1.517436,0.12615 2.046904,0.170015 2.31061,0.341873 4.987851,1.161474 6.575826,2.189531 0.002,0.0013 0.0041,0.0025 0.0062,0.0036 4.044961,2.350387 7.887107,5.171765 11.042737,8.476485 0.437545,0.618765 0.582799,1.046559 0.55087,1.299146 -0.01606,0.127073 -0.06823,0.214164 -0.158129,0.286804 -0.0899,0.07264 -0.221794,0.128427 -0.38499,0.162264 -0.652781,0.135351 -1.783159,-0.06818 -2.632397,-0.220659 -0.002,-7.56e-4 -0.0041,-0.0014 -0.0062,-0.0021 -3.240763,-0.404906 -5.958496,-0.22944 -9.406144,-0.348815 v -5.17e-4 l -0.09767,-0.01395 C 17.337383,26.965149 14.715516,27.064952 12.218892,26.874845 9.7244921,26.684908 7.3569537,26.207747 5.0157145,24.638806 l -0.00207,-0.0021 C 2.7859128,22.881058 0.49029103,18.648227 -0.28938802,15.430066 0.11301099,15.288976 0.66336152,15.183434 1.3161987,15.111222 2.2445981,15.00853 3.3797811,14.971016 4.6002363,14.976347 Z m -5.078243,0.527616 c 0.79735528,3.263213 3.0791565,7.488254 5.3707316,9.292973 0.00185,0.0013 0.00375,0.0025 0.00568,0.0036 2.3795944,1.596656 4.7920441,2.082454 7.3044641,2.273763 2.090631,0.159192 4.253052,0.117742 6.534485,0.341065 -3.505014,0.09906 -7.512284,0.573565 -11.0752935,-0.487826 l -0.00568,-0.0021 C 5.5655029,26.146926 3.3604156,24.731717 1.697054,22.867338 0.0322564,21.00135 -1.0893059,18.688096 -1.0330119,16.109611 c 4e-7,-1.72e-4 4e-7,-3.45e-4 0,-5.17e-4 4e-7,-1.72e-4 4e-7,-3.45e-4 0,-5.17e-4 4e-7,-1.72e-4 4e-7,-3.44e-4 0,-5.16e-4 4e-7,-1.72e-4 4e-7,-3.45e-4 0,-5.17e-4 4e-7,-1.72e-4 4e-7,-3.45e-4 0,-5.17e-4 4e-7,-1.72e-4 4e-7,-3.45e-4 0,-5.17e-4 4e-7,-1.72e-4 4e-7,-3.44e-4 0,-5.16e-4 4e-7,-1.72e-4 4e-7,-3.45e-4 0,-5.17e-4 4e-7,-1.72e-4 4e-7,-3.45e-4 0,-5.17e-4 4e-7,-1.72e-4 4e-7,-3.45e-4 0,-5.17e-4 4e-7,-1.72e-4 4e-7,-3.44e-4 0,-5.16e-4 4e-7,-1.72e-4 4e-7,-3.45e-4 0,-5.17e-4 -0.00643,-0.121456 0.034697,-0.223592 0.13074139,-0.326078 0.090961,-0.09706 0.23512261,-0.190757 0.42426381,-0.273369 z"
       sodipodi:nodetypes="sssscsccscccssscccccsssscccccccssscccccscccsscccscccssssssssssssscsc" />
       
       <path style="fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:square;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="M 0.70374001,15.236402 C 2.819355,19.959065 11.291099,23.545712 14.938411,23.260775"
       id="path105612"
       sodipodi:nodetypes="cc" /><path
       style="opacity:1;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 1.5196645,15.602432 c 3.621165,3.492958 6.1543303,4.130374 10.8854765,5.017879 3.192828,0.722016 6.714479,0.357497 9.732625,1.702146"
       id="path105614"
       sodipodi:nodetypes="ccc" />
       
       <path
       style="opacity:0.901683;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:square;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 4.7043572,22.297464 c 2.0503866,1.625236 3.9895179,2.024813 6.4602978,2.558403"
       id="path105616"
       sodipodi:nodetypes="cc" />
       <path
       style="opacity:0.901683;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 12.982314,31.074525 c -1.769964,1.307409 -4.9683604,1.69293 -4.9683604,1.69293"
       id="path105618"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.881396;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 7.3121397,42.77321 c 2.8164703,-2.176726 6.0324903,-6.346719 5.9395623,-9.257275 -0.07731,-1.081937 -0.404324,-1.765422 -0.687843,-1.392525 -0.635477,0.835807 -3.4887542,2.113141 -6.8971862,1.981183 -6.48610908,0.143142 -9.9789288,2.643867 -10.8198134,7.618737 -0.4099401,3.66471 -0.3535982,6.247873 0.5888761,9.499517 1.0494796,3.596589 1.8731228,1.977845 3.83076711,-1.049188 C 1.0463286,46.797999 4.7345014,44.680008 7.3121397,42.77321 Z"
       id="path105620"
       sodipodi:nodetypes="ccsccccc" /><path
       style="opacity:0.687215;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="M 6.0999801,40.367238 C 5.0376329,41.210812 4.4333147,42.861485 4.4364888,42.883211"
       id="path105687"
       sodipodi:nodetypes="cc" /><path
       id="path105676-2"
       style="color:#000000;opacity:0.887018;fill:#100c09;stroke-linecap:round;stroke-linejoin:round;-inkscape-stroke:none;paint-order:stroke fill markers"
       d="m 12.46875,34.279297 a 0.10001,0.10001 0 0 0 -0.08008,0.04297 l -0.06055,0.08984 c -0.01669,0.0224 -0.02025,0.03478 -0.05273,0.06445 -0.06236,0.05695 -0.151692,0.122674 -0.259766,0.19336 -0.216148,0.141372 -0.508178,0.300821 -0.828125,0.466797 -0.639894,0.331952 -1.3909555,0.686222 -1.8886719,0.972656 a 0.1,0.1 0 0 0 -0.035156,0.136719 0.1,0.1 0 0 0 0.1347656,0.03711 c 0.4839408,-0.278506 1.2358363,-0.634137 1.8808593,-0.96875 0.265905,-0.137941 0.491107,-0.268299 0.697266,-0.394531 l -0.978516,1.421875 -1.2285155,1.644531 a 0.1,0.1 0 0 0 0.019531,0.140625 0.1,0.1 0 0 0 0.140625,-0.02148 l 1.2285155,-1.646485 a 0.10001,0.10001 0 0 0 0.002,-0.002 l 1.392578,-2.021484 -0.0039,-0.002 c 0.0037,-0.0091 0.01469,-0.01583 0.01758,-0.02539 A 0.10001,0.10001 0 0 0 12.4688,34.279204 Z m 0.248047,-2.195313 a 0.1,0.1 0 0 0 -0.09961,0.09961 c -0.0089,1.336435 -0.226114,2.808891 -0.583985,3.890625 -0.256041,0.773936 -0.589688,1.411599 -0.820312,1.800781 -0.09527,0.160771 -0.156577,0.249083 -0.203125,0.316406 -8.72e-4,0.0013 -0.0031,0.0046 -0.0039,0.0059 -0.03507,0.04868 -0.05553,0.075 -0.06836,0.09766 -0.0017,0.003 -0.0056,0.01301 -0.0059,0.01367 -1.39e-4,3.31e-4 -0.0078,0.02522 -0.0078,0.02539 -1.3e-5,8.6e-5 0.0039,0.04683 0.0039,0.04687 1.6e-5,4.6e-5 0.08004,0.0664 0.08008,0.06641 4.3e-5,6e-6 0.05852,-0.0078 0.05859,-0.0078 7.1e-5,-3.3e-5 0.01553,-0.0097 0.01563,-0.0098 1.97e-4,-1.45e-4 0.0095,-0.0076 0.01172,-0.0098 0.0045,-0.0044 0.0077,-0.0073 0.0098,-0.0098 0.0083,-0.0099 0.0141,-0.01953 0.02539,-0.03516 0.0069,-0.0095 0.03011,-0.04767 0.03906,-0.06055 8.75e-4,-0.0013 0.003,-0.0046 0.0039,-0.0059 a 0.1,0.1 0 0 0 0,-0.002 c 0.05013,-0.07237 0.114892,-0.164705 0.212891,-0.330079 0.236285,-0.398735 0.575868,-1.047829 0.83789,-1.839843 0.367241,-1.110056 0.584682,-2.594218 0.59375,-3.951172 a 0.1,0.1 0 0 0 -0.09961,-0.101563 z" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.4;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 19.421656,46.828592 1.645418,3.294157 c 2.851419,7.04363 2.695406,11.062194 -0.161374,16.65001 -3.951541,6.117151 -5.504947,18.08796 -7.893543,10.225535 C 12.513401,74.768318 11.666896,72.601879 11.161722,70.529081 10.207595,66.565849 10.081384,62.215 12.697461,58.550586 15.41484,55.391112 18.363407,47.416508 19.335886,46.789219 17.944061,39.998285 14.925002,33.914424 11.833125,27.777974"
       id="path105803"
       sodipodi:nodetypes="cccccccc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 17.613662,49.703184 c -2.76049,2.118002 -3.681139,5.197574 -4.671825,8.472057"
       id="path106531"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="M 12.088299,59.499798 C 8.2418804,65.968797 9.0586969,72.667111 13.570461,78.63733"
       id="path106533"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 20.135713,48.052167 c 3.956354,7.980509 5.926558,8.415519 1.798182,16.613447"
       id="path106535"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 18.355807,65.563188 c 2.997972,-6.282396 2.798239,-9.548825 1.073456,-16.046217 0.520813,2.606108 0.06198,4.990426 -0.378676,7.554413"
       id="path106537"
       sodipodi:nodetypes="ccc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 23.729514,39.400702 c 6.009878,0.04352 9.691053,-1.002565 15.29671,0.552822 -1.080321,-2.596078 -3.252713,-6.286012 -3.489816,-8.543586 -0.09078,-3.442909 3.307792,-1.855917 4.990959,-0.691285 3.073178,2.133079 5.436138,5.179743 4.68475,7.926052 -0.920647,2.830892 -4.244148,4.446326 -6.382512,6.319737 0.456464,-1.275212 0.522753,-3.186163 0.196619,-5.010918 0.30086,1.476829 0.287076,3.301514 -0.196619,5.010918 -1.191006,2.887566 -3.00051,5.833711 -6.145023,4.200716 -1.547915,-0.824484 -3.039294,-2.483294 -4.195923,-3.745115 -1.730862,-1.893829 -3.214614,-3.789819 -4.759145,-6.019341"
       id="path106539"
       sodipodi:nodetypes="ccccccccccc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 37.211592,45.716004 c -3.982114,-0.860786 -6.610213,-3.173729 -9.962054,-5.088382 1.475763,0.690404 2.910911,1.526808 4.48622,1.859383"
       id="path106541"
       sodipodi:nodetypes="ccc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 30.784009,44.381486 c 1.837005,2.528295 3.391759,3.060339 4.862863,2.731582"
       id="path106543"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 51.547154,51.997345 c 3.263062,-2.493299 6.26375,-4.27151 9.238456,-5.517392 5.076325,-1.67305 8.733182,-2.61473 12.676114,-2.501071 4.032783,0.386961 7.608911,0.607238 10.445427,3.659016 1.150182,1.269255 -0.469737,1.468739 -2.770226,2.470123 -2.898877,1.326009 -5.781487,2.652971 -8.467406,4.321634 -1.6926,1.280624 -2.651245,1.989313 -3.662884,2.436372 -3.892291,1.473125 -8.156162,0.877027 -11.729538,-1.005707 -1.840068,-0.987796 -3.568233,-2.057328 -5.729943,-3.862975"
       id="path106545"
       sodipodi:nodetypes="ccccccccc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 63.228005,45.70141 c -3.002343,1.671552 -6.754369,4.269925 -9.920318,6.270162 7.55894,5.975939 11.154921,5.04432 19.361832,2.458083"
       id="path106547"
       sodipodi:nodetypes="ccc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 68.369531,51.787919 c -6.053783,1.638752 -9.093841,2.628058 -13.965413,-0.516849 2.597246,1.209711 5.129965,0.583908 7.917742,0.523588"
       id="path106549"
       sodipodi:nodetypes="ccc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 68.677519,44.342201 c 4.328975,0.04222 9.074548,0.544422 12.876281,1.439154"
       id="path106551"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 60.600994,55.181163 c 1.20572,0.338665 2.335449,0.285769 3.555836,0.178493"
       id="path106553"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 43.809122,51.317386 0.358445,1.324907 c -1.113732,7.79312 -1.609559,9.804126 3.966475,15.515376 2.392328,2.285123 5.130047,4.953785 7.956964,6.646895 2.695955,1.380956 3.43136,2.308132 3.223881,-1.138835 C 59.083079,70.076777 57.166239,65.827565 55.983057,63.305848 51.313701,53.308115 43.809122,51.317386 43.809122,51.317386 Z"
       id="path106555"
       sodipodi:nodetypes="cccccccc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 44.167567,52.642293 c 0.644435,5.586947 -0.474378,9.979908 3.983945,15.414604"
       id="path106557"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 47.672241,61.277949 c 0.338766,0.976602 0.616478,1.969377 0.88324,2.967098"
       id="path106559"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 52.401422,63.668134 c -1.279562,-5.145416 -4.7324,-8.945248 -8.335604,-11.396187 1.362248,1.413453 2.771105,2.768003 3.548111,4.166836"
       id="path106561"
       sodipodi:nodetypes="ccc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 36.172207,29.577199 c 1.950211,5.632389 4.522351,9.80128 3.234495,14.88102"
       id="path106563"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 40.794558,35.559364 c 1.008149,1.812816 1.859385,4.329768 0.985002,6.950721"
       id="path106565"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 36.872503,29.296536 c 3.936901,2.999686 8.056403,6.21409 7.682237,10.689484"
       id="path106567"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 24.044154,56.179152 c 3.977464,2.573242 7.186566,5.887296 9.761113,9.431058 2.673276,3.703583 4.627794,7.751913 4.858675,12.172417 0.03481,1.502173 -0.445518,1.876423 -1.062844,1.56547 -0.911994,-0.930786 -1.943437,-1.7523 -3.029222,-2.543415 C 29.24236,73.635943 24.799851,68.64418 21.933895,64.665614"
       id="path106569"
       sodipodi:nodetypes="cccccc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 21.44132,65.946064 0.678196,0.843153 0.66107,0.824452"
       id="path106571" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 23.901013,69.028949 c 1.887197,2.631615 4.219996,4.283247 7.468369,5.608158"
       id="path106573"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 23.635182,64.442461 c 1.132249,1.673157 2.639518,2.5809 4.36979,3.495342"
       id="path106575"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 23.801013,60.634948 c 1.345754,2.22613 4.449568,5.101019 7.452332,7.754363"
       id="path106577"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 25.820077,57.408107 c 1.707102,3.126841 5.787626,6.656189 9.054901,9.765492"
       id="path106579"
       sodipodi:nodetypes="cc" /><path
       style="opacity:0.911409;fill:none;fill-opacity:1;stroke:#100c09;stroke-width:0.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 12.668899,32.135193 c 0.564296,-1.004897 0.274197,-1.967577 -0.08417,-2.915694"
       id="path107307"
       sodipodi:nodetypes="cc" /><path
       style="opacity:1;fill:none;fill-opacity:0.941176;stroke:#100c09;stroke-width:0.6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 11.907851,27.926302 c 2.046068,4.123668 7.543755,8.709338 11.821663,11.4744"
       id="path109131"
       sodipodi:nodetypes="cc" /><path
       style="opacity:1;fill:none;fill-opacity:0.941176;stroke:#100c09;stroke-width:0.6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 37.6215,47.831027 c 4.728886,0.628289 9.099672,2.932556 13.925654,4.166318"
       id="path109133"
       sodipodi:nodetypes="cc" /><path
       style="opacity:1;fill:none;fill-opacity:0.941176;stroke:#100c09;stroke-width:0.4;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;paint-order:stroke fill markers"
       d="m 44.147983,53.673144 c 0.01958,-1.030851 -0.633201,-3.295145 -1.255891,-4.553775"
       id="path109135"
       sodipodi:nodetypes="cc" />"""
        # 1. Eliminar atributos sodipodi e id que rompen el XML embebido
        paths = re.sub(r'\s+sodipodi:[^=]+="[^"]*"', '', paths)
        paths = re.sub(r'\s+id="[^"]*"', '', paths)

        # 2. Reemplazar el color hardcodeado por el color primario en todos los estilos
        paths = re.sub(r'stroke:#[0-9a-fA-F]{3,6}', f'stroke:{primary}', paths)
        paths = re.sub(r'fill:#[0-9a-fA-F]{3,6}', f'fill:{primary}', paths)
        # Restaurar fill:none que no debe cambiar
        paths = paths.replace(f'fill:{primary};fill-opacity:1', 'fill:none;fill-opacity:1')

        svg = f"""<svg viewBox="0 0 92.644897 70.955803" xmlns="http://www.w3.org/2000/svg">
            <g transform="translate(6.4691908,-10.338102)" {rotate_attr} opacity="{opacity}">
                {paths}
            </g>
        </svg>"""

        return "data:image/svg+xml," + urllib.parse.quote(svg)

    def render(self, data: dict) -> str:
        """Recibe los datos como parámetro y genera el HTML"""
        
        titulo = self._safe(data.get("titulo") or data.get("nombre", ""))
        descripcion = self._safe(data.get("descripcion", ""))
        eco_text = self._safe(data.get("eco_text", "100% NATURALES Y ECOLÓGICOS"))

        font = self.config.template.font_family
        primary = self.config.template.primary_color
        bg = self.config.template.background_color
        product_image = data.get("product_image")
        color_img = "#6b2348"

        branch_tl_url = self._branch_svg_url(color_img, opacity=0.9)
        branch_br_url = self._branch_svg_url(color_img, opacity=0.45, rotate=True)

        html = f"""<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <link href="https://fonts.googleapis.com/css2?family={font}:wght@400;700&display=swap" rel="stylesheet">
            <style>
                * {{ margin:0; padding:0; box-sizing:border-box; }}
                body {{
                    font-family: '{font}', Georgia, serif;
                    background: {bg};
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0; 
                    box-sizing:border-box;
                    overflow-x: hidden;
                }}
                .wrapper {{
                    position: relative;
                    width: 100%;
                    height: 560px;
                    border-radius: 20px;
                    overflow: hidden;             
                    box-shadow: 0 20px 50px rgba(0,0,0,0.15);
                    border: 1.4px solid #d9c8a5;
                    background-color: #ffffff;
                }}
                .wrapper::before {{
                    content: '';
                    position: absolute;
                    top: -40px;
                    width: 340px;
                    height: 290px;
                    background-image: url("{branch_tl_url}");
                    background-repeat: no-repeat;
                    background-size: 100% 100%;
                    z-index: 3;
                    pointer-events: none;
                }}
                .wrapper::after {{
                    content: '';
                    position: absolute;
                    bottom: -20px;
                    right: -15px;
                    width: 230px;
                    height: 190px;
                    background-image: url("{branch_br_url}");
                    background-repeat: no-repeat;
                    background-size: 100% 100%;
                    z-index: 3;
                    pointer-events: none;
                }}
                .img-half {{
                    position: absolute;
                    right: 0; top: 0;
                    width: 52%; height: 100%;
                    clip-path: polygon(16% 0%, 100% 0%, 100% 100%, 0% 100%);
                    z-index: 1;
                }}
                .img-half img {{
                    width:100%; height:100%;
                    object-fit:cover;
                    display:block;
                }}
                .content {{
                    position: relative;
                    z-index: 2;
                    width: 55%; height: 100%;
                    padding: 1.4rem 2rem 5rem 2.8rem;
                    display: flex;
                    flex-direction: column;
                }}
                .spacer {{
                    height: 200px;
                    flex-shrink: 0;
                }}
                .titulo {{
                    font-size: 3rem;
                    font-weight: 700;
                    color: {primary};
                    line-height: 1.08;
                    margin-bottom: 1.1rem;
                }}
                .descripcion {{
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    font-size: 0.95rem;
                    color: #444;
                    line-height: 1.75;
                    max-width: 360px;
                }}
                .footer {{
                    position: absolute;
                    bottom: 1.8rem;
                    left: 2.8rem;
                    right: 48%;
                    border-top: 1.5px solid #c8b89a;
                    padding-top: 0.8rem;
                    text-align: center;
                }}
                .eco-text {{
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    font-size: 0.82rem;
                    font-weight: 700;
                    letter-spacing: 0.12em;
                    color: {primary};
                    text-transform: uppercase;
                    line-height: 1.5;
                }}
            </style>
        </head>
        <body>
        <div class="wrapper">
            <div class="img-half">
                <img src="{product_image}" alt="{titulo}">
            </div>
            <div class="content">
                <div class="spacer"></div>
                <h1 class="titulo">{titulo}</h1>
                <p class="descripcion">{descripcion}</p>
            </div>
            <div class="footer">
                <p class="eco-text">{eco_text}</p>
            </div>
        </div>
        </body>
        </html>"""
        return html