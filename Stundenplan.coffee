# This is a simple example Widget, written in CoffeeScript, to get you started
# with Übersicht. For the full documentation please visit:
#
# https://github.com/felixhageloh/uebersicht
#
# You can modify this widget as you see fit, or simply delete this file to
# remove it.

# this is the shell command that gets executed every time this widget refreshes
command: """
  export LANG=de_DE.UTF-8
  cd /Users/Shared/Ubersicht/Stundenplan.widget/
  /opt/local/bin/python3 Neuer_Stundenplan.py
"""


# the refresh frequency in milliseconds
refreshFrequency: "1s"

# render gets called after the shell command has executed. The command's output
# is passed in as a string. Whatever it returns will get rendered as HTML.
render: (output) -> """
  <span class=out></span>
  <div class="bar-container  container-hour">
    <div class="bar bar-hour"></div>
  </div>
  <div class="overbar overbar-hour"></div>
  <div class="spacer-hour"></div>
  <div class="bar-container container-day">
    <div class="bar bar-day"></div>
  </div>
  <div class="overbar overbar-day"></div>

  <div class="spacer-day"></div>
"""



#afterRender: (domEl) ->


update: (output, domEl) ->
  #Liest Zeit aus und gibt prozentualen Fortschritt der Stunde zurück
  perc = (line, len) ->
    linelen= line.length
    min = parseInt(line.charAt(linelen - 2) + line.charAt(linelen - 1))
    hour = parseInt(line.charAt(linelen - 5) + line.charAt(linelen - 4))
    time = hour * 60 + min
    return parseFloat(100 - time / len * 100)

  #Funktionen, um die domEl-Inhalte zu manipulieren
  hidehourbar = () ->
    $(domEl).find(".container-hour").css "visibility", "hidden"
    $(domEl).find(".overbar-hour").css "visibility", "hidden"
    $(domEl).find(".spacer-hour").css "height", "0px"
  showhourbar = () ->
    $(domEl).find(".container-hour").css "visibility", "visible"
    $(domEl).find(".overbar-hour").css "visibility", "visible"
    $(domEl).find(".spacer-hour").css "height", "44px"
  hourbarwidth = (perc) ->
    $(domEl).find(".bar-hour").css "width", perc+"%"
  hourbartext = (perc) ->
      $(domEl).find(".overbar-hour").text perc+"%"

  hidedaybar = () ->
    $(domEl).find(".container-day").css "visibility", "hidden"
    $(domEl).find(".overbar-day").css "visibility", "hidden"
    $(domEl).find(".spacer-day").css "height", "0px"
  showdaybar = () ->
    $(domEl).find(".container-day").css "visibility", "visible"
    $(domEl).find(".overbar-day").css "visibility", "visible"
    $(domEl).find(".spacer-day").css "height", "44px"
  daybarwidth = (perc) ->
        $(domEl).find(".bar-day").css "width", perc+"%"
  daybartext = (perc) ->
       $(domEl).find(".overbar-day").text perc+"%"


  #Parst output, liest letzte Zeile in args-array aus
  arr = output.split "\n"
  arrlen = arr.length
  args=arr.pop()
  args=args.split ";"
  #Weist args Variablen zu
  hourlen=args[0]
  daylen=args[1]

  #Erzeugt output mit <br> statt \n, ohne letzte Zeile (args)
  output=""
  for line in arr
    output+=line+"<br>"

  #Wenn gerade eine Stunde stattfinded
  if arr[arrlen-3].substring(0,19) == "Diese Stunde noch: "
    hourtime= perc(arr[arrlen-3],hourlen)
    #Lässt Balken erscheinen
    showhourbar()
    #Prozentzahl übergeben
    hourbarwidth(hourtime)
    #Als Ganzzahl gerundet ausgeben
    hourbartext(Math.round(hourtime*100)/100)
  else
    #Lässt Balken verschwinden
    hidehourbar()
  if arr[arrlen-2].substring(0,11) == "Heute noch:"
    daytime = perc(arr[arrlen-2],daylen)
    #Lässt Balken erscheinen, wenn positive Prozentzahlen kommen.
    #Sonst hätte der Tag noch nicht begonnen, die Uhrzeit wäre zu früh,
    #die Differenz wäre damit negativ.
    if daytime<0 then hidedaybar() else showdaybar()
    #Prozentzahl übergeben
    daybarwidth(daytime)
    #Als Ganzzahl gerundet ausgeben
    daybartext(Math.round(daytime*100)/100)
  else
    #Lässt Balken verschwinden
    hidedaybar()
  #Erzeugt den Text-Output neu
  $(domEl).find(".out").html output



style: """
  bar-height: 1.55em

  background: rgba(#fff, 0.65)
  -webkit-backdrop-filter: blur(5px)
  border-radius: 8px
  border: 2px solid #fff
  -webkit-border-filter: blur(5px)

  box-sizing: border-box
  box-shadow: 5px 5px 5px rgba(#000000, 0.25)
  color: #141f33
  font-family: Helvetica Neue
  font-weight: 300
  font-size: 110%
  left: 1%
  line-height: 1.5
  padding: 10px 10px 10px
  top: 1.5%
  min-width: 360px
  text-align: justify

  widget-align: left
  .bar-container
    width: 90%
    height: bar-height
    border-radius: bar-height
    float: center
    clear: both
    background: rgba(#fff, .5)
    position: absolute
    margin-bottom: 10px
    margin-left: 5 px
    margin-top: 1.2 ex
    border-radius: 100px
    z-index: 1
    overflow: hidden
  .bar
    height: bar-height
    float: widget-align
    transition: width .2s ease-in-out
    height: 1.55em
    z-index: 2
    text-align: center
    border-radius: 100px

  .bar-hour
    background: rgba(#00c27b, 0.6)

  .bar-day
    background: rgba(#009C63, 0.6)


  .overbar
    width: 90%
    margin-bottom: 5px
    margin-left: 5 px
    margin-top: 1.2 ex
    text-align: center
    z-index: 3
    position: absolute
"""
