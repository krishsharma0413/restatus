import datetime
from threading import Thread
from time import sleep
from requests import get
from json import dump, load

def updater_main():
    while True:
        with open("./database/all_links.json") as file:
            data = load(file)
            for x in data:
                resp = get(x)
                if resp.status_code == 200:
                    data[x].append([datetime.datetime.utcnow().ctime(), True])
                else:
                    data[x].append([datetime.datetime.utcnow().ctime(), False])
        with open("./database/all_links.json", "w") as file:
            dump(data, file, indent=4)
        sleep(500)

def updater():
    Thread(target=updater_main).start()

def html_writter():
    a = ""
    ascri = ""
    buttonnumber = 0
    operational = []
    with open("./database/all_links.json") as file:
        data = load(file)
    for x in data:
        al = data[x][-30:]
        a += f"""
        <hr style="opacity: 1;">
        <div id="status-page-div">
            <h1 id="status-page-heading" style="font-size: 25.52px;font-weight: bold;">{x}</h1>
            <div class="row" style="margin: 0px 0px;">
        """
        operational.append(al[-1][1])
        for y in al:
            buttonnumber += 1
            if y[1]:
                a+= f"""
                <div class="col" style="max-width: fit-content;padding: 0px 0px;">
                    <div id="button{buttonnumber}" style="background: #05ff00;padding: 15px 7px;border-radius: 3px;margin: 13px 0px;margin-right: 4px;max-width: 10px;"></div>
                    <div id="tooltip{buttonnumber}" class="visually-hidden tooltipss" role="tooltip">{y[0]}</div>

                </div>
                """
            else:
                a+= f"""
                <div class="col" style="max-width: fit-content;padding: 0px 0px;">
                    <div id="button{buttonnumber}" style="background: #ff0f00;padding: 15px 7px;border-radius: 3px;margin: 13px 0px;margin-right: 4px;max-width: 10px;"></div>
                    <div id="tooltip{buttonnumber}" class="visually-hidden tooltipss" role="tooltip">{y[0]}</div>
                </div>
                """
            

            ascri += f"""
const button{buttonnumber} = document.querySelector('#button{buttonnumber}');
const tooltip{buttonnumber} = document.querySelector('#tooltip{buttonnumber}');
""" + f"""
button{buttonnumber}.addEventListener("mouseover", funcbutton{buttonnumber}, false);
button{buttonnumber}.addEventListener("mouseout", funcbuttona{buttonnumber}, false);"""+f"""
function funcbutton{buttonnumber}()  
""" + "{" +f"""
    tooltip{buttonnumber}.classList.add("visible");
    tooltip{buttonnumber}.classList.remove("visually-hidden");
    """+f"""
    Popper.createPopper(button{buttonnumber}, tooltip{buttonnumber},""" + """ {
        placement: 'top',
    });
}
"""+f"""
function funcbuttona{buttonnumber}() """ + "{" + f"""
    tooltip{buttonnumber}.classList.add("visually-hidden");
    tooltip{buttonnumber}.classList.remove("visible");
"""+"""
}"""

        a += """
            </div>
        </div>
        <hr style="opacity: 1;">
        """
    if False in operational:
        operational = """
        <div>
            <h1 class="fw-bold" style="text-align: center;color: red;background: #00b4ff;border-radius: 8px;">MINOR OUTAGE</h1>
        </div>
        """
    else:
        operational = """
        <div>
            <h1 class="fw-bold"  style="text-align: center;color: BLACK;background: #00b4ff;border-radius: 8px;">EVERYTHING IS OPERATIONAL</h1>
        </div>
        """

    return (ascri, a, operational)