## NOTES FROM THIS EXAMPLE
## Duplicate from parent, only cascades to child.
import platform
import ctypes

# Fix Bug on Windows when using multiple screens with different scaling
if platform.system() == "Windows":
    ctypes.windll.shcore.SetProcessDpiAwareness(True)

from pathlib import Path

p = Path.cwd().parent
import sys

sys.path.append(f"{str(p)}/pysimplesql/")
import PySimpleGUI as sg  ## pysimplegui 4.60.4

sg.change_look_and_feel("SystemDefaultForReal")
# sg.change_look_and_feel("SystemDefault1")
# sg.set_options(font=('Helvetica', 12))  # Set the font and font size for the table
sg.set_options(font=("Roboto", 11))  # Set the font and font size for the table
import pysimplesql as ss
import logging
import time

custom = {
    "ttk_theme": "xpnative",
    "default_label_size": (10, 1),
    "default_element_size": (20, 1),
    "default_mline_size": (30, 7),
'delete': b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAFbUlEQVR4nIXVW2wcVx3H8e+cmfHO7O54b4nt2Ln5kmzjKlWJol6gASUppRE3qRJSJS6i4qq2NDVyhfoAEqVQQECFKngAERKFBxTRklSq3KYJbZWWXBwTokDiS9aOnaS+7Hp3dvY2O7NzhgdI5UZp+T8e6f85R38d/f4KH1LPQ3YQtibT8SzJVHeoKIQVZ6G4ZE9egvPDMP5BvcqtDp+Dvu0pa6j3vh0PJLdt25zIZtFMkzCUtKpVKtPTFP8xNjV54u1jZ0qVX/0QLv8/WDmoi0e2fuyeZ2//7OfWaH39EEgIAUIIQkKhougCgoDW7AwXXj68NPb3se9/w/f/AAS3hP9oak9+Ys+eX/Tu3q02XRc8n0CoFByHUtUhJKQ9GqUj3o6mCIgYGIZO7tjr4dGR155+1G39nP894z3414b+xU/u3LF/YNtdmu04hLrKQn6ZM+fPe1fm5uYqTW/RB9SI2tF/W7Zjz/a7E11CoYVCor2dqdOngiNvvvPNp31/H4AG8BR0b9rc91xPz3otNzGJahrMzF7hxJmxU1Nu84V34K1rsAyENIj9db54wJLhZ0rLBQLfx15YYP2GDeodA9d//NClqeMvwawG0GWZj2U7u9ZN5XK4qkrtWpW3zp47dLwVPHEaFlfOzU5lvlMZ6N3p5Cbway7EY9QbLna+wGB3V9fWq3NDL1WbQ9rD0NmTST9QW7a5XK2yKpng35NT/3y9FewdXYECXE0lhvN9a3/m2MuiVXEQ6QzjmXWo4xNEK1UicYvN6eTOweriOi2jssUM/C25q3OUFYHie37OrvxmFBZWohOx2ONOqv1HpaV3hazViaQyHHfs5bf/9uaxjYH36buDMD5RLBJVxZbtKrdrkUhkIO37sQtFGy9mQuAvjMDRlegbUWM4H9d/4ucXdel6aAmLV/1G5eXry0O2K4+IqDjXGypxzZf0R0090aZlha2qKUdKroQhNaDu+aVpmL+B7je1vb6hPluvVXW/6SHa47xhRCoji/bwWVcezIEjhVaoajouIT4SHyUlKshQCsG8ojDuezSC4L0v+Iwhvoem/NJzG5Gm30KJmpwRwnmtUHzsZNP/HYAEReqaktd0ZiQsKAoFRZHC8bxCSxVsUgVqEBCEQWItdDwa4wlTCZ8JWr5aCCSerjEtKY/Z1SdPuvLgjcu/BmtMw+hoSIkAhKJQa7Vsrd6UkzO+LA7qarroBuhWrPOR/q5D0dzlO7tD2aYAlipoBpTH641vH5L8eeX8K5r2+Y3R2FpRKtPXplKCRtGTF4UDF6dd9+JAPM56wGj5kWyt+tF+KaMxFDqFStoPa1eare8+fxO6C3p6ujuGNnq+utoLyJoGs63g0jz8S5wHe7LePDyjKtxr6MQaDdquvYuhCtqjJqulWLruh48PS/atRB+CvnvXdB64y4pusvIFPhJRKQhBruaNzMG8BjDfkvuOVmpf2ptO3Ll1qciirqBrGtZAlhN5+8L+mZnRDZAMQbkHercZxv2Znu5vrY239YWzs1gyIJmyeNFpTJwNw9++L4R2wK5dKesvX49HUmWnwoIQEI8TtJlSCWRBDym3CY0wGk0IQ+8I6xXc/CKZVkDSNNlfc+sjTuMrp+HF98EA98HD96fbX/hqylpl+j75MERPJLAS7RimiRAqTc+napdolsskZUBdUfhTsVJ+xak/NQq/X5kr3ITvviMa+emD6dT2j2/oIWJZRKImimGAUMDzaFZrOPllTl1f4NWifeGc6/3gJBxe6dxyNQGpT8GXN+n6FwYzqdv6O1evSlkWEFKqVMgtFpYni6XJi55/5Cgc4KZc+TD4RmW2QzYJgyYkQlA8KJdgYvS/i3Tpgxr/A2+Df04FIOdTAAAAAElFTkSuQmCC',
    'duplicate': b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAACxklEQVR4nJ2VT08TQRjGn5lZoBVMTIxGTBRjIARI1APGKxg/AXjlyGfg4NXPwrXBCwdCQmwUQgjEA5gWWygtbenS0tJ2/87O66Hddss/WZ/kvUzefeY3z7yZZbhF8/PzHxYXFz9xrgnGiPx1pQClJKRU177p6xM8n89XV1dXl7XbjEdGXj+Znf34tb+/77aWG5VOp0vb29vfrxpHlpaWnuq6zoaGom8tyyKlFFPqOt1NikYjkFI6pilJW1hYeDw393l+dHT0TX+/9iISibzSNK26s7PzjjHGqJtCKGlENDw+PvZlYmLipb/oui4ikQjuS3qTeCwW0zWtrwgAhmHCNC0YhgEpPRApEFGIChA3m80Lx3ELV3dkDCAClGqZ30fdE7rQADjlcjnted1jE3VNwxqrdisHgEQimbIsEwDgtc18Q6XCV8d4c3Mr7XnKJiKQCpPp9QK1Tq4BwP7+r4xtO070QXTApwV8gnBR+L3tKBL5avVCZ5xDdSYB/0/tG9dqtVqhWMhoQnTyVdQuFa48L2AMgM6KxUPOeCDj1niEIW1dHHUzBoB6vZ6Snmw3KFCbgLEwGXudWe4Yc85Tl7UacaG134eWWTC3f4mIQOiNArZtZyqVakNwDs9TnXm8rxhjYIwBxFgP8fr6enl6+n1RiOGHPqFhGBBC6yH2iUAA4wyCczDGQUTgnMOVbmujwKaPfm5txaYmpmYqlQqSySRKpbMWRZtGcA4hBDjnUESwHRvScZHNZn84jrsshBi4bNbr8Y2NWPChv2w2GodENDM4OIjJqUmMjY3ClR4c14F0XKder5v6ua7nTk+Pzwr5VLlcTktJmWTy93Y8Hj8KRhM0Vrls9mD42XPLtEzdlW7JNs2iruupRCLxZ29v7/jg4OAol8sVG43GBQDvrsx7fk1ra2vfTk5OjnZ3dzMrKyvnACoAjLsMbtNfF/q/W8NpHj0AAAAASUVORK5CYII=',
    'edit_protect': b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAA3mlDQ1BJQ0MgUHJvZmlsZQAAeJxjYGB8wAAETECcm1dSFOTupBARGaXAfoGBEQjBIDG5uMA32C2EASf4dg2i9rIubjU4AWd5SUEJkP4AxCJFIUHODAyMLEA2XzqELQJiJ0HYKiB2EdCBQLYJSH06hO0BYidB2DEgdnJBEdBMxgKQ+SmpxclAdgOQnQDyG8Taz4FgNzOKnUkuLSqDuoWR8QwDAyE+woz8+QwMFl8YGJgnIMSSpjIwbG9jYJC4jRBTWcjAwN/KwLDtaklqRQmy5yFuAwO2/AJg6JMRgPgAAGRFOS2P6Ey1AAAD5klEQVR4nJWVTWhdRRTHf2dm7n33vtfcpG1SDSm2SqvWhmykEUpBtJQitlIXhVbcqQtLV+5VXCu4at217kTophQ3UhDBD1BESi3SRrQNIf0ir3nvJS/vfsyMi7nPtC4kHhiG+fqd/5wzH0JtZw+w+cV3Pny+MfrEiDLGoQGjAQ3aoNGgh21CbQAMYgtZvX99Yc+x934B8eARgAsnx3e/cOTUma07p/erqJEi2qM0ohQoXRcFMqzrfpG6Rqxz99q3589vP/D6B0AlHx+i9dqhE188ve/lo6z0Af8oQAS0CUVUPa7COGp9XiOlao5x89aN07tfeeuMmSrYk9lilvZ9sO4h4LpaW/QpyxzRhqg5iopSENYdiIJiDeNyVK99dDucM70lWuXifIMdz0LlQK8r8UBnpU1/ZCu0RsE7pL3ImDak2UTYzT9wASrav/3YXIDUVEDRWYK1HjjWY6kV/aqA2WNMzhwMyQDKok/vuy8xd+aIkix0Kh0c+Ir87oLPAIMBl6/BYGU9SVrjrUXvfYnmzEGY+x5u/gpxk2jmMNn+49ivz8LqMqgIEDAxLM3jFq5BBsYY8GKh6ocEEeAikEzuAlfBlUuw0gYcpE3M7An0xBR0FkAnYYcrPfjpIqyuwvZaMdqDH4CvwV7jvUV8BbbC+wFel+AtYtcQ74EyrBEN1QCuXYbOPBILWdcHxSomTMKAGMqyZLkyjHihIbCUV9h+Ac6SFpZMoJtX2G6bsdYA9efP0J6DZgy9EroeYxJQkQdyEAt2DTvxHOn+00TbdiI6ZtOr7+OdBTy60QIP6b7jFNuewl04herdgmYK1qKjkGZDAhIDkoNU4AuSySdh6pnhbSfZ/Bj/trg1SrxjGloR9E0IYyWoRgVYjElBxx7UAJQBXwb1GzFnoaEh0eAUaI+OVa3YgG4MFVtQJahqY2AhQFMNVoMVdKMGR8agIgmKRYMUwGDj4FgH1VUAq+gRxQK6BF2BysG4DYIVNEyAKw0OTBSGTJKATiRsSSvQDtwyeF/f//8wuwp6AImBUoGFONFkGRjXTLwkCRgJnuMmdH6AK+9CshXE1Y8N4AHnQ7HAg+tAB5JGfVQ9Lk1F97refHtDLe7dNXZvS8YY1aonigRTwPLl4ExL/WMQHinroPRQ2qAy1uF0VA7SLSwU3T+udlgxn17q/jU1fuf8G0emP5p8fDImthDXcYsUGFW/vbXiagh2kFeQW8gtLo+48vuDW598dfscUEo9f9Pbh7M3Dx3YdbTZ2pR5JeHTUoCq4+yHcfXgwVsHDrwFrJfFO3dvfnZx7vOr83wDuIezo4FxIH0I83+sAywPG38DjMiDuqlxCFcAAAAASUVORK5CYII=',
    'first': b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAEdUlEQVR4nJ3VW2xURRgH8P/MmbN7dk93z263l13aQrdcItUALoiRID4AJmKiJkJEjS9oomhIiT6pSYmIFvCCt/hkMDHxBZ9MlKiJqUQjJoIRFI1WC5QApWW73Uv3XObMfD4stGCQFL/Xb+Y3/7kkw/A/asu7J57q7YitHPjsXF9x/+rqlb0H9xxb291qrRM3JK7/0uYW62tJWc8OF6XvnfDiAGbgew8+2pGJ7RQmy84e3nQoH+XqzfWruh7Idzfjxf2/nJ6yL/UeHmxhgexfvbRta+/CjHjl41/rs4KNh77ZlLT5zlxh/k3FpTkcqPqAwQmJqi82D66IGXgju2L+GmNVFz73A1Q9l10f3vZD0poMtqcz9gttt+Wj9Y40TvtAsk5gpqGFnXoi7Vh92UK+M1zQhiHFkKj44ILjP+HI44cXR+rhO9lFbevs5d0ox6LQAWAKgDMNJakj15EayKxaKKppG4EEBAdMwcAMdg14B3Hr7OGNdkwMZBfne6gngwluAK4G4wy6ruCOVtDc5RixW3vCUtwS5BE4AAIDEcCMfyV2+gZTcuzHfidjb2u9uUvUUjb8KQVGEmAAaQ1d85GwTbhNWZoICUbFm55PnIP8EOBXwPHtRwoA293e6ayPdqYwIQTUpAsGgC6NYaRhcAafC3g1H8Q5acZmYMaglWwkvmuQxPdf/LzZJPF6NpdqDxMWJjwN5tavQi9XyBg4CBSE0FM+wK+AwUBMNRJ/t+/4vsLC5JN3rnXMr897GK24IE1Xgf9egAzWgJUGGJ/uEhjIROPyzGbjZFnoi6PVMNcdlWAswGg5hC81oAmkCYwIWhM4CGAMoWVCAZChBicA1BhHihA6JmAYaOxjx2+FJsXfWzTHvmN+inC+5GLkYohqXYGIAA1AawgOGJwhGhVwNZNBIENois3AGq2OhSk55U4fUNPzf7bCRH82FdnSmxVx3w9wclyiVFMIQwJpDQNAk8WQTpgoB5C1ehhqTTGlqLE7pdHiRFHzKjPw9Ot4eeixRCSy95bOWNYxPAyPBxgtKQRSg4jAGUNPexR2nMuxchCWqhSToYZSBFKqAdevAQNAfNdQIWJG9uQz0XV5R2O84mOkqFBzFbQiNNkCLTbCuZmovFANY+dKITyfECqFTFMEtdrktWEASO+ecCTKL7UmzKeX5KKm73kYHpco1TSSRohSrRq0NCdEb3eaV2sBThUlaq5CKi5QqVwHBoBNB8g4ODKyMRE19i5qi8/NCB/DRYnAkyi5/l8Vjz50LP5c77yWZluEGBrzoclAuVS6Pny5Um+dWQLGB+Zl4hvunsNAgY+PjhX/loXFy92vvl1mJZy9C7pzK2/PCRgAPjly1uWzgSe3dx1nVuyRU5PuwNER7Z/8yYL0hGHWL1jea2sORXLt9/1+euyD4TMBTQ3F4dcZZpX4qvRvj9+fGzZfHRNSmGvl6tENc8YBAEQs2X90a/tY146iqKdv7M8DMNnX+mlyV+mMqLNloxf8mf+OMaoA7yef+WNCWO33/AN4qR0EolKhAgAAAABJRU5ErkJggg==',
    'insert': b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAADgklEQVR4nKWUS4scVRiGn3Or6qrqmk7PLZlJZjJJBMULkiCEKOgqC1f+guz8K+JWxH3AlT8hIIoQL4tINolR1NiZybRz6bl2dVV3Xc45LuIigumR8YNvd97nO4fzva9gSnXe7VxdvXj+dlYMFyaT2uE8sU7k+bnlvd72+oebdzbvvUirp4GPh8cvXXrlnTeuv3VdDg+OkCiWFpe5d/f+0t37310BTgfG4Q45tPFKJCs1QZeaeDbmz2HfUmKnSaeDFahY4GNH2S6oJpJiUuDVVBUA8qQDKlGEcYiKFVVSMvElXlk4AX4yOFaEkUGFEhs2VGqCFe5/3thSyhZII/Ha08iGUpR4YcFSTpPqG7duXN3Y773W3902KDzB3+OePfVqZCIaGmpqKldS+glz8/NCnOGmf5NZHDABLFAhVtdW62tXrv0sLr5/4fPFG7O34tWYbvsMaadNErWJdYJQsHRuybvYiac76xwNDkirOZbVCk82epRlhXIS2UhwkkAF1FnF91/98IUeHA+MUCXxckhy1pCeXWTpzDlmghTvIcsysbe3x1F+wGiUU+xUjGRGFEV0ZhICbdDyWUdBxNbjbbYGW0ZTeZdtjtjvDBjmx2wN+8x35um2usSyja9gnI0ZHY+wuw6ZG+qkIsdglMEojcaga0NURRwW+zSmcZpaQC6x6zCsM+qi5qh9hDEagUTVmqBsER3HhGWEnnXIrieIFSaQGGVQSLCO2pU0+zUiAt0OZ1T8ssQtlSAFdashDzOEEVjrwUlkP8DuWOaudFhbvMzKwmXaUZtW0EJLjfQK7zx4EIUhnW0rvba8tj/+NV/f/nHPSylAChCA9i4wJnn7g/cWn3R7opf/AnHFQrvLbn+LL79+tOOUz4X3EgfU4CrHhe6KWD13cU8/ePzw4/Fg/Bk1nuftL7DFfH1z8Pr+J/KSNGYeOp0OaWeGjd979vE36x9xyB30cx4s4UnQF7TI9PjBePOFW77Aq3mRo2JPkBiSOCFNUgbiyCPo8we/nc55Di1qgTBgAk0YhrTCFkoqkNPT4sSs8BNACKSQSPms/0NUnJgV+Bq891hnaWyDtRZb/fM7/q2m5zEIjRbCe2pnqWxF5UpkIwUecWpw3E6LVh66yd0KXYTkTyv6G7uY3cil3bTIyE4HTsP40cbD3qejb4dpJWt/0MrZig9Ed2Z21I27P00D/wXiuYpflIypzwAAAABJRU5ErkJggg==',
    'last': b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAElElEQVR4nJXSeWhcVRTH8e+59773ZjIzSSZp9tgmqY3dXNCKIlb/UOtSBEHqgvSfVtA/rFVa3HDBqkhBFBQUBIvgiqIiaMGiVKtYq9KqYItW7aIm6ZJkJpN5M2/mvXv9I6nWVKUeuH+dy+f8OBzWbfrh8Ws3fnsJM6p11We5J97+ZdOqZ76/dWbvZEoZT93e05p+nuWbbzq+Uf2+2vDLaP3yWc2pR9XVW+7jsg8y/wt+9dMhFs5rHVh6XveLcu2Wp7lx6yyAcgZe//xQvb+vpfWqS/sfC1q8l1nxSf9Jw6VqRd6PAvTFC82pS+auyWneMjdsXUKuFKGVe6MUMHr2AHOXDl6Tz6nN+vqPV5wUrIxi74Rjb+Jhzu+n7+IFF+XzqXdMpvlm8bQdDh0HIkV9cQ+zL1k0v70r91Jq5bYHWfNF43/CogXPCMbBZCyE8zroWXZ6b1dP8+NJ3fUosXgKohoUu/O0L1sU9A62P5wN47f81dsX/AescA6cBZU46lXHeC5D49L5ccspTboyMoENY7COpGIZMz7+uXOZc86pl+YazHupmz+/joecOgFGKVwUk5RrJGGEDSOSiSpjscP1dbp0xiM5MoEthbhKhJuoUiwnVHrz9Jw7dyDfmnml4fBXTzSt3dp8QmJbq2PLVew0bMMIV45cNawRaYNWggtr2HING9Zw5SqVQoUxY2ha2GM6elvuRBrfaLjj67OPweZYYuscgvtzorUOVYuJQ6GGIM4xs+rAmChyHU10NgSXjQwXzvDu3rX+givOet2Ilim4Hh8HC9ZZJE5wzmGTv1ABZo6YVEJno2L1aV0dn35U3PTZU9+dZ9Ca+EiRWrGOaEGUgAhWAKOIgbhaB+ewCEoJTqb/KSHwFJ0thjmBz0jJUDT2qNei9xlRgkscNokRFOKmYJQgaIxy+FpI7NTlOGQqNpBLKWbPMnTl0/xcEH4cKmyfTNnbeHHxToMWxDco30O0AiVoPZUs22Bo8mG8BJPVqQWIUhgj5LOa/jaPIPDZNRKHI4XaJhK1gUfnHwEwojXiTT+t0VrwjCKfE9qbfMqhZbJgscahRPA9RWdeM9DmU0xSfPNrZaRUq98Vbhh86fi9G1GCGI0KDEZrUoHQnTd05AwHRyM5WgYrgjKKbFozu1XT1hiwr6jYN1r5sFav3R0+MG/nzIsxaIXyFF5gyKY1fa0euazP7v3jwdGxUpzP5jCBIZ9VDLR5BKkUu4aj+pFS9KxH00Ph/S3FE+4QUE5p8AwtzR6LTkmDn2LH3rGx30rJA34uc9Bv8Ohu81nUmybUGXb8Hh08XElWXjnQt278nn9Gp3csXD6YIQF2DMf8tH/oy2qpeFd62dJv7M49q5YPZhE/YMuQ48BouBnn7i2vn/Pdm/8mHoOjUCjvbWAoVXB7fj/6Qqar4/7Cg2cearxwpKNeNXrfzhTj3Um0f7L6pEqlN47f8u8p/77jsYzZdrh4+FD7bw+XN5zzXFnEASjPWjWRr+2O3e7hTHJfcW33uycDHitlUvnXKqawduKRJc8yjQKMHIpKJpCN5Ta3srC27X+hAH8AdlXicmbovD8AAAAASUVORK5CYII=',
    'next': b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAADU0lEQVR4nK3ST2hcVRTH8e899743k5lMJplOmjQTYxLbgpZY4yIUJFoUxQqFIhWFigqtO4m0KAE3Id0WS0RBilj/FFcKCmoQBVvBRWxLUrUINqSEQjNpMmmSl8zkvZl577kYhaRJTBM9cBaXC5/749yjWFaZ5869+Nje9FmnHP/6m+/mexg6eJMtliw/3MzO1M/SYO3vvO/Zpt2JLzj4/b7/BUarcGjMQTJJHj3UsS+Zjn1rv/BjDy+fj/4nWCzQtuGzacPldIq2Ax2pxkztQLSo3osd+WnH1hMjKBHCENwizKVrqH1yj7p3b/NRE7UGzSsXurcIA0ZQUrkIyzBn2eiudtoe2flQbXX8K/voz8fpO282B4tGaQV+SFgKCEs+uD6OG7B4T5rm7l2phsbaU/Fs7MOqY0PNm4BBiSLwygQFj2Cp0hQ8luZdcpEoyYdbddOuhpfsmD0Yf+3K43cFixaU1oReiaBQXNEUPAJniZmlMkEmSWZ3Q0esis/jPSPH6btqb5gYEUK3hJ/3Kqnv6HDRZWGhiBO1SLdvT9Wk4qdtx/80eepK27/AAlrhe2X8grdOFwnzLq7jUggCuh9McPiBhudLl/Rg9bGrh/+hVv6ugNKK8uQcxVkXEUEpQBQohRJFqBRGC8lqTUvCEFdRpr0QiWhHmTC/NowGERRAEIIKKq+FIShFGIBlQX1SaN9uIdrih5Ec2dn5D+o66/tyJ/Zk14Y1KC2I0SjbVFbv76RKhFhE2JEytGyzyeXh15Hrk4vO/Em/ZfhM7kR/sJxaAQuVrUALytIoERCF1opETGhNW2yriXBtymds9MaQjidfL7+z/+KdG7E6salAGI1YGiUKyxLqE4bWtAXa4pc/st6tialz0caaXqe/8/Za6BozBoxCGQFjqIoKTbWalnSEnGvx2+/jk54vbxXPPP1RcT1x/RlrAq1JJEJ21hvqqqP8mS0wPn59OCguvFoYODC8gbkaDgBlhI6WKoLAZzG0uTg25U9PTL5vSoWThXefmb4bdHViEfxA6IpWc6Nc4uNLo7dL87O9vW8/cbZfqWAdY2M4YivlTVh8cs1lOjV6Ib8492Z54KnL/ac3Q66V2Kq7VZqccfJR70vuz7xRPtKV2zxZqb8AZ5dPS7TL3K4AAAAASUVORK5CYII=',
    'previous': b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAADVElEQVR4nKWUbWiVZRjHf9d9389zXndOPu5sbmdzNlm2xHAFKUElQbGyYYTRB4lCLOyNoi99EcaQXkCCYUFFggR9qj4EfRAMMoNk6rJpQxpTe3G6DbepZ67tnPOc++7D5tirzXV9eZ6Hi+d33/z//+sS/k9t/i77VHN6f8qMtRw9PbTz0tfPf3mzpZYNbTm8ufqusm+2NK195iqV3qX+4czMtrlt4AtHon7evRyL+a0PtzQGKhuh49te0OKWDY7vOFplC25vRTa9M9i0VjrLU/ReyaN9g/LALgdsXvzxIaO9/VUNFRsjG2u55vuEBUg5EKWYq+p/g1uPGL/PeyMVi+zJ3lcXFNeUc80JEoJSIAow8626JTi2q6NG9cu7warEjpX31ujRIEV+wqIcOMApAesQLaD00sCJ17seNcq2V9QGGyL15Qxpg70+gcJNa+lEsFJClMzL13xwa7efuFp8LR5hT6auMsgHcYbHQ8QWgdkGORGcsYjWKK0WNy+9r+vO8cul91NB4rk7KpPkPENhtIByjllZmiqL4CJMir3YjZO7urcXT7q92x/L3B2udBzvLzGRm0BwlBBYAG0RSmjQMglfCCxGxlRE5XL5IhkR6v0J/s6FXL9RIixZxDmcdeAcWDf5sJZwRXTKvNmHTn+Ofrr+ULSJpw/1XPj8+1+HKIv6NFZ5VKQVngI37djNSNjJRDAlBXphMMDQ2/f0l4Ifdg9c/OvVnzovDIyGhsbaOGuqoyTLPJRvEN+Ar5Gpd+VrRKu53AWWUFubDQ9u+8Qm0ts6uy929I4IdZVxGrIR0imD9g3iGcQYxNOg1WQq5qAW3W6595pO6LTa+vuZsweOnx3MJxIx1tfEWBX4+FGNeArlaTAalMybvluuzVzbgyOFz5pfGh53r/z8W9/AKDHW1cRYnfGJxT0wBjEKjMz7d0n7+J8P7j+YHxva+svpnlM9gwVWVyRYV+1TVmawWiNaL0HjxeDtT5xiPNd87tyfH584P1KKJJNsqo+zYXUMMbOn7rbAADc+evLKOx8+8ubw5b7dx878MVLtx3kgmqRk1eIDstRqE7HAAfPW4a6vjpX2ZUYatuSTHhFfJFzujWdW2P54J43ZZ8fC818UB4ZzeCsGZ/b/BS8ZGtkt5XZMAAAAAElFTkSuQmCC',
    'quick_edit': b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAEQklEQVR4nJWVW2xUVRSGv733XGk70JYpFTWlNlViQLwgCY4XaIgiqCHVxCgkJmCqJvigREwMaah4iT4QHmg0SCipoISEixglQisB2noBFCg0NUDptKQtw3TamTLTuZxztg/DTKcpJbqSk5Ods/e3//WvlbMEY+EEJP8/dP2ysvKn7fN26ljc0vHRD+e1tJwQma/r169/paam5s1EMqkBRO5RIbJrDQit0QKEdGCMBnR+z9v36JPOubF9YULJeJ99JLzSljlbUlo6q6Ki4rmb0ShCSqQQCCGQQqTBGXj2rbDMBML/Nb06yHt/OZgVivJCdGhm0BR1WbBlGEYikSAajaKkAsE48LgLhESjMP2fE/d/y6adUzh21uSxiiFerLTMwSPiT9tYviqtVEqkkll1MgvLgCUIhdnXgA58z+Z9Bfz8h2Z26QB1qy2KpsqGjReNz7LFUgqklGnALSuUEAil0nAlUVKilBMzeBhnqJGGw272NCmK3UE2rUmQ57a1vr/V+KKlnZtjXWCaCEBmQFKOeS0lSkikcmBETuMM7eBgq4Nth0ycIsRHr4WZv+AZth/3HT/yO9cBMws2c1OHbPoZsJQOrNhlnMFttF5QfNkYJjE6zLqXB1nku59A3gcYrocSwChg5ViRVpp9Mn5LiVIOrFQQdaOBf/wGn3wzQCA4RM3zg7xUVUKvWgvu2RRNc40CBkBO8cZ6NrdgQtrAiCBvNHKtb5gNW/1c6grw+qJh3ljupke8RcLxONOLPRQXF6cyGDmemZu6RCkb6BR6cD8jwwPUfXWFU+19LJ0/wrvVKXr1qwzqhRQX5VFUVIjdbue24Aw83WoSsNCDh4iFOtlY30FzWzdPPhhjw6oYAZbhH62isNBDWVkZUo5HTQTf6gYhQIeOYEVOs7nhIoearjBnVoraVUNE1ALOh5ZQUFBAxX3leDyeCY5O8FgAQtpIhjswenex/UCAxoPXuNdr8unqYRyeB2jyL2Oat5DKygq8Xi+GYWCz2TC0FpODb/kcjyX4+7KXXT+epTDfpHbVEDNmzGD/xWexHC4Kpxbgcrvo7+9HSok7L4+RSCQ5KRghMFMxIqFeCjweVlRNp7K4k7mVDr47sxjLXUr5zBJ8Ph8ulwutNYZh0NTU9MsPBw78NCnYpmwM9F0i1H+GxHA7Tz3iYtrUKjqSj/Kwz8fdd03HbndkfbUsi9bWltb6+vp3zp071z25YmDv/sP0dp5gZfUTlJQvJd87jyn5HlxOG7FYjOvXAwAYhkHbb22nduxoqDl69OjVOxYvHB5CCMHCJWuZs3gFTpcz+5M3TZN4PI5lmViWxcmTx9v27Nm7Zvfu3Z23EwjAli1b1un/EMlkUnd1denm5uZfq6uXV07Gyyru6em51tHRcQzQQgi01hM2W0AikRLtF85fraut/bi7u9s/GTh3tE0B7KTH2p1CAHEgcadN/wKKN8qJ5UwIfgAAAABJRU5ErkJggg==',
    'save': b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAADnklEQVR4nJWVTYsdRRSGn1Pdcz8m1zs3RjNG3Ki7iAkDBmEwxESJ4geZX5G/4MI/4FIXLhQE3erGlQuDQQJBRJQIQaMgxGRM7s2YkMjNdHfVOadc9L2TmVFwLChO01Q99dZ73qYFePTwM0c/6fYWV0+8ePyvE8dXG7cs7HGEINycbIQPP/jood6+vi/2+2+dP/fFxyXw7OJg+NKhQ090VlZWltbOnNkrc2tcvbbOp599zoFHlvnm4vkjACXgOaNVVXdiTKg6f9y4ich/i845M9o/oqpqzBIxNojgczApJeq6RtVx4OEDB/astixLkipmjpnhbmyBc86YG+bO/c2Gm3tU7NkZjUYkddxbcKt3DjbH1EiqeM6M9u/fs+KiLGliwt1JSefcFmyuuBtuzmbVMB6P2YNgssPSaIiao6aYKb5dsXueKTY0w3Bp9L8Ux5hwc0yVuRczsGE283hasTGZ7E1xhoeGA9RmHquSfQe4vcp0OqXb6/LY44fIObebyf8ACg9OXeh0uHb9OpoSyf5Fcafb5eKFC9xYv05RhHa7gEjYqhnI7m3NTvaMCEwmEzrdPpbaPm2BzQyRwO3bdxiPJwDEmAghUBRFGz0RyJnsmUzG3SnLkiIEJAjdXg/VXaloo9IgQeh0OywfPMjpl0+xtDTE3Agh7DJA8Oyc+/Irfr7yC25Q15uIBNzzLo81kQFV4+iRwxx/4Rjvvvc+V3+/xqmTJ3nzjVe2fAeh1+tw69aYS5cv0ylLqs2KTre302NVQ5MBGVMlpcT6+jrffvc9ngt+uvIrx55bQWatzNnpdrtUVUU2x4OTc0ZTwnV3KjTRHqI0TU1d14gI0naMpqmZr53Xpq4xU0TAzQkyd3ireQlNCcioG01sqKsKTQnNgaZpaJqGnPOWHSIQUyJqmr1zJMgOcJHdF1S1tcIMjUpMipkRY8Tcqapq9lE8yLWpYSlR5AwSSCnh2zy+GmP8oVzQ50UgpUhVbRJCweuvvUpV1Tz91JM0TWyv7I6IUIRAjA0pJoIIORuqEVct5+DfNu/fe1tT804oioUiSP3nxuTepR8v9fu9Thjs68rduxvhzp2NNg7tyGVZ5vH4Rk/T/YOulXt2cdNGJHy9fSFnz55dWFtb6y8vLw+Gw+GimS0OBoOBiAyKouiHELpAURQFgLp7E2NsVHWzaZppmk6nd6uNe6urpzdEZOdPM+cswMJsdrc9l0CxXTGgs5mAuK2aiPjfVyVxPnamx+cAAAAASUVORK5CYII=',
    'search': b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAEKklEQVR4nKXUX2gURxwH8O/M7t7e3u79y/1Pzpg/mliNljQpCrW1ptam0D6IVRCF1pBXi0j0JU1C6IuI+GSlL0LbpxKFFsEg0lQEQ0wpLYRAizHVnjF3Fy/3/2737nZn+qAWGri0NF8YmIHhw/dhfkOwJleufNcTCbgP2B1yl80m2SVJTFLCZn5fSN8ZHDy4vPZ+vZCXm/7jY66j+7uHg+HQCaq6G22qw1RkkcNiIjGrUATr50wuM97Xt+fmf4QJTp0ade14ZedXWjB6SIg2l1raAizopMQpgNQsjkTW5NlkVmlAqVTM5c68ue+1qwAnAOH1YApwEo20DjPZeyjtb8uEOyNEVkSxalFasCipQCBOjywomwPlGPMQzeW6MDk5/foLlNSFT5++1CPa5E+WpOaMKxKQCkVGClXwAgMKJpCrAdkqOKNULDtdZryiuEJ+z7mJiQmBkHUaO1XxwDNdchvu5opehpIvUeTLQKEK5C2QggWhUAXJ5oGaJcoP8koOgtRrWZ4Ozuu6EJnFdy4V7PGZGXK/3zR3dWwSIxaDrFfBCYFumqhyQDYtOIoViAnDntNr1LMp4m0F8FtduFo17TpntViOpaZ+Ne8m0lzbHBI0VQGv1FAs6ahYDLIq84hDFbbndMKrJpMkcHvdugBEwzBWVHvZ1R4lYkfYRv1uoaQqKHpUCrsNlAHI5FFeXmULi3Ez5oTeKkXNXalMKb0urBu1e5qYGmxxpLzBQGO6JcjEaIjyoBuwyUDNAlIZENVOqW5RvdtWbOCmEV9cXJ5fD6bLieIUq+TnosWf9ng9QDBAWZMfaPYDbW6gxQNsCgI+H8x2dzaw1ZXb9iyZvjk0dDzFwes/t8nJi4n0s/yItPrQR+en9mq2itDkQy0swgpTsJAIK+hGzVnL+HfgcZ+Cql3VtBoAkHUGhLxY/MSx0ZOuBuelUGuztb23c76rvSnpU2xmKl9yPH662l5MZbZUCmUlHPYjZ+BbdXZgcptjbql1GHfqwSCEgHOOw4fP9vr9vnNer7tHc6peTZNFKgg6YXxFN4yJVCq75A1E3m3Rkkff7vqDq8b91ZWZ6YEto5jk/DnzD3htjhz5rNPnc7dpimS3QNJzj+LzU9+fXwWAs/1dA8cO0qvdHw1yhJpI8e6FeGJ6dmDrOG5xgBCg/tSsl4v99r0zZ6W4daOLW7HLjFeu8eytPcmHI3gfADiv/3/8a8YPqO/MDtEn7EYX50+uMF65zgu3dy8/Gn+Obyhj+9W+2SHx6XP8MuPGNZ69/UYydh7vjQH0/9cGMNKn7v+g2/im963OKO39lMNtI7Hrl6dj8d0fihuBP/+xdIda6kmQB1/38C8a/xQPYkEbob80NtINwQAwfrf0g0OWTyykEmNLUb+oK/zL8eHdqxt1/86+Vz/2RDrO+F+e/wJfqs7yOu4sNgAAAABJRU5ErkJggg=='}

ss.languagepack(ss.lp_monty_python)
ss.themepack(custom)

tables = True  # Set this to False to use sg.Combo for selectors.
sz = (900, 300)  # for layouts
grandchild = False  # Set this to False to only be parent/child
quick_editor = True  # quick_editor=quick_editor
enable_id = 1  # to see ID on tables.
_tabs_ = "-TABGROUP-"
foreign_keys = False  # toggle to False to see default behavior

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO
)  # <=== You can set the logging level here (NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL)

sql_grandchild = """
CREATE TABLE IF NOT EXISTS "bike_repair" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Bike Repair Placeholder',
	"example"	TEXT NOT NULL DEFAULT 'True',
	"bike_id"	INTEGER NOT NULL,
	FOREIGN KEY("bike_id") REFERENCES "bike"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "service" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Bike Repair Placeholder',
	"example"	TEXT NOT NULL DEFAULT True,
	"bike_repair_id"	INTEGER NOT NULL,
	FOREIGN KEY("bike_repair_id") REFERENCES "bike_repair"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);"""
sql_grandchild_insert = """
INSERT INTO "bike_repair" VALUES (1,'Wheel Repair','True',1);
INSERT INTO "bike_repair" VALUES (2,'Seat Repair','TRUE',1);
INSERT INTO "bike_repair" VALUES (3,'Seat Repair','true',2);
INSERT INTO "service" VALUES (1,'Basic',True,1);
INSERT INTO "service" VALUES (2,'Premium',TRUE,1);
INSERT INTO "service" VALUES (3,'Gold',true,2);
"""

if not grandchild:
    sql_grandchild = ""
    sql_grandchild_insert = ""

sql = f"""
CREATE TABLE IF NOT EXISTS "person" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT DEFAULT 'Person Placeholder',
	"example"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "car" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Car Placeholder',
	"example"	TEXT NOT NULL DEFAULT 'False',
	"person_id"	INTEGER NOT NULL,
	FOREIGN KEY("person_id") REFERENCES "person"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "bike" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Bike Placeholder',
	"example"	TEXT NOT NULL DEFAULT False,
	"person_id"	INTEGER NOT NULL,
	FOREIGN KEY("person_id") REFERENCES "person"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "building" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT DEFAULT 'Building Placeholder',
	"person_id"	INTEGER,
	"example"	INTEGER NOT NULL DEFAULT 1,
	FOREIGN KEY("person_id") REFERENCES "person"("id") ON DELETE SET NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
{sql_grandchild}
INSERT INTO "person" VALUES (1,'Bill',0);
INSERT INTO "person" VALUES (2,'Jessica',0);
INSERT INTO "person" VALUES (3,'Drake',0);
INSERT INTO "car" VALUES (1,'Landrover','False',1);
INSERT INTO "car" VALUES (2,'Jeep','FALSE',2);
INSERT INTO "car" VALUES (3,'GTO','false',3);
INSERT INTO "bike" VALUES (1,'Unicycle',False,1);
INSERT INTO "bike" VALUES (2,'Street Bike',false,2);
INSERT INTO "bike" VALUES (3,'Moped',FALSE,3);
INSERT INTO "building" VALUES (1,'Tower',1,1);
INSERT INTO "building" VALUES (2,'Mall',1,1);
INSERT INTO "building" VALUES (3,'Cabin',1,1);
{sql_grandchild_insert}
"""

# -------------------------
# CREATE PYSIMPLEGUI LAYOUT
# -------------------------

# Building
# -------------------------

# Define the columns for the table selector
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True)
    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("person_id", "Owner", width=20)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "building",
            sg.Table,
            num_rows=4,
            headings=headings,
            auto_size_columns=True,
            alternating_row_color="#f2f2f2",
            row_height=25,
        )
    ]
else:
    selector = [ss.selector("building", sg.Combo)]

building_layout = [
    [sg.Text("Buildings - Childless Parent, default int 1")],
    selector,
    [ss.field("building.person_id", sg.Combo)],
    [
        ss.field("building.name"),
        ss.field("building.example", sg.Checkbox, default=False),
    ],
    [ss.actions("building", default=True,)],
    [sg.HorizontalSeparator()],
]

# Person
# -------------------------
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True)
    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "person", sg.Table, num_rows=4, headings=headings, auto_size_columns=True
        )
    ]
else:
    selector = [ss.selector("person", sg.Combo)]
# Define the columns for the table selector
person_layout = [
    [sg.Text("Person - Parent w/ cascade, default int 0")],
    selector,
    [ss.field("person.name"), ss.field("person.example", sg.Checkbox, default=True)],
    [ss.actions("person", default=True)],
    [sg.HorizontalSeparator()],
]


# car
# -------------------------
# Define the columns for the table selector
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True)
    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "car", sg.Table, num_rows=4, headings=headings, auto_size_columns=True
        )
    ]
else:
    selector = [ss.selector("car", sg.Combo)]
car_layout = [
    [sg.Text("Car - Child of Person/ Sibling of Bike, default str False")],
    selector,
    [ss.field("car.name"), ss.field("car.example", sg.Checkbox)],
    [
        ss.field("car.person_id", sg.Combo),
    ],
    [ss.actions("car", default=True)],
]

# bike
# -------------------------
# Define the columns for the table selector
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True)
    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "bike", sg.Table, num_rows=4, headings=headings, auto_size_columns=True
        )
    ]
else:
    selector = [ss.selector("bike", sg.Combo)]
bike_layout = [
    [sg.Text("Bike - Child of Person/ Sibling of Car, default bool False")],
    selector,
    [ss.field("bike.name"), ss.field("bike.example", sg.Checkbox)],
    [ss.field("bike.person_id", sg.Combo)],
    [ss.actions("bike", default=True)],
]

# bike_repair
# -------------------------
# Define the columns for the table selector
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True)
    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "bike_repair",
            sg.Table,
            num_rows=4,
            headings=headings,
            auto_size_columns=True,
        )
    ]
else:
    selector = [ss.selector("bike_repair", sg.Combo)]
bike_repair_layout = [
    [sg.HorizontalSeparator()],
    [sg.Text("Bike Repair - Bike child, Person Grandchild, default str True")],
    selector,
    [ss.field("bike_repair.name"), ss.field("bike_repair.example", sg.Checkbox)],
    [ss.field("bike_repair.bike_id", sg.Combo)],
    [ss.actions("bike_repair", default=True)],
]

# service
# -------------------------
# Define the columns for the table selector
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True)
    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "service", sg.Table, num_rows=4, headings=headings, auto_size_columns=True
        )
    ]
else:
    selector = [ss.selector("service", sg.Combo)]
service_layout = [
    [sg.HorizontalSeparator()],
    [
        sg.Text(
            "Repair service - Child of BikeRepair / Grandgrandchild of Person, default bool True"
        )
    ],
    selector,
    [ss.field("service.name"), ss.field("service.example", sg.Checkbox)],
    [ss.field("service.bike_repair_id", sg.Combo)],
    [ss.actions("service", default=True)],
]

# -------------------------
# Main Layout
# -------------------------
print(ss.themepack.ttk_theme)
layout = [
    [sg.Button("Form Prompt_Save", key="save", use_ttk_buttons=True)],
    [sg.Button("50 selector switch test", key="-timeit-", use_ttk_buttons=True)],
    [sg.Button("Display all", key="-display-", use_ttk_buttons=True)],
]
layout.append([sg.Col(person_layout, size=sz), sg.Col(building_layout, size=sz)])
layout.append([sg.Col(bike_layout, size=sz), sg.Col(car_layout, size=sz)])
if grandchild:
    layout.append(
        [sg.Col(bike_repair_layout, size=sz), sg.Col(service_layout, size=sz)]
    )

layout.append([sg.StatusBar(" " * 100, key="status_bar")])

window = sg.Window(
    "People and Vehicles",
    layout,
    finalize=True,
    grab_anywhere=True,
    alpha_channel=0,
    ttk_theme=ss.themepack.ttk_theme,
)

driver = ss.Sqlite(":memory:", sql_commands=sql)  # Create a new database connection
frm = ss.Form(
    driver, bind_window=window, prompt_save=ss.AUTOSAVE_MODE, save_quiet=True
)  # <=== Here is the magic!
if foreign_keys:
    driver.con.execute("PRAGMA foreign_keys = ON")

frm.set_prompt_save(ss.AUTOSAVE_MODE)
frm.set_fk_column_cascade("bike_repair", "bike_id", update_cascade=False)
window.SetAlpha(1)


def test_set_by_pk(number):
    for i in range(number):
        frm["person"].set_by_pk(2)
        frm["person"].set_by_pk(1)


# variables for updating our sg.StatusBar
seconds_to_display = 3
last_val = ""
new_val = ""
counter = 1
# ---------
# MAIN LOOP
# ---------

while True:
    event, values = window.read(timeout=100)
    if event in (sg.WIN_CLOSED, "Exit", "-ESCAPE-"):
        frm.close()  # <= ensures proper closing of the sqlite database and runs a database optimization
        window.close()
        break
    elif ss.process_events(
        event, values
    ):  # <=== let PySimpleSQL process its own events! Simple!
        logger.info(f"PySimpleDB event handler handled the event {event}!")
        # handle button clicks
    elif event == "__TIMEOUT__":
        # --------------------------------------------------
        # Status bar updating
        # --------------------------------------------------
        # Using the same timeout, we can update our sg.StatusBar with save messages
        counter += 1
        new_val = frm.popup.last_info_msg
        # If there is a new info popup msg, reset our counter and update the sg.StatusBar
        if new_val != last_val:
            counter = 0
            window["status_bar"].update(value=new_val)
            last_val = new_val
        # After counter reaches seconds limit, clear sg.StatusBar and frm.popup.last_info_msg
        if counter > seconds_to_display * 10:
            counter = 0
            frm.popup.last_info_msg = ""
            window["status_bar"].update(value="")
    elif event == "save":
        frm.prompt_save()  # Prompt save when tabs change
    elif event == "-timeit-":
        st = time.time()
        test_set_by_pk(50)
        et = time.time()
        elapsed_time = et - st
        print(elapsed_time)
    elif event == "-display-":
        frm["bike"].requery(filtered=False)
        frm["bike_repair"].requery(filtered=False)
        frm.update_elements()
    else:
        logger.info(f"This event ({event}) is not yet handled.")
