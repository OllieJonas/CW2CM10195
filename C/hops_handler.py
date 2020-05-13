from subprocess import Popen, PIPE
import re
import platform

UNKNOWN_COUNT_THRESHOLD = 20


# Executes traceroute command for the website given
def execute_traceroute_command(website):
    result = []
    unknown_count = 0

    process = Popen(get_traceroute_command_syntax(website), stdout=PIPE)  # 255 hops
    print("Executing Traceroute Command for " + website)

    for line in iter(process.stdout.readline, ''):
        if line == b'' or process.poll() is not None:  # If stream has finished
            result.append(str(len(result)) + website)
            break

        else:
            line_str = "".join(chr(x) for x in bytearray(line)).strip("\n")  # Convert byte stream to string
            line_str_split = line_str.split()

            print(line_str)

            if len(line_str_split) > 0:  # Fixes Windows bug of returning empty strings
                if "* * *" in line_str:  # Ensures we don't end up with too many unknown hops
                    unknown_count += 1
                    if unknown_count > UNKNOWN_COUNT_THRESHOLD:
                        process.kill()
                        print("Traceroute for " + website + " has been killed - too many unknown hops\n")
                        return None

                elif line_str_split[0].isnumeric():  # ie. this is a hop
                    result.append(line_str)

                else:  # ie. any other random stuff that the traceroute command prints (don't want this in the list)
                    pass

    print("Completed traceroute for " + website)
    return result


# Returns the syntax for the traceroute command based on OS (Windows has a slightly different format to UNIX-based
# operating systems.
def get_traceroute_command_syntax(website):
    if is_windows():
        return ["tracert", "-h", "255", website]
    else:
        return ["traceroute", "-m", "255", website]


# Removes any http business or anything at the end (eg. https://, http://, .nz?, .nz/)
def format_website(website):
    return re.split("[/?]", website)[2]


# Reverses list
def sort(results):
    return sorted(results, reverse=True)


# Returns a boolean for whether the platform running this script is Windows or not.
# (Included this because I use both Linux and Windows)
def is_windows():
    return "Windows" in platform.system()


if __name__ == "__main__":
    websites = ['www.bp.com', 'theyardchch.nz', 'muffinbreak.co.nz', 'muffinbreak.co.nz', 'www.frobisher.co.nz',
               'www.bp.com', 'www.majestic.org.nz', 'www.cnmc.org.nz', 'www.stmarysaddington.org',
               'www.chchstmichaels.org.nz', 'www.jcf.org.nz', 'www.jcf.org.nz', 'samoanaddington.adventist.org.nz',
               'www.methodist.org.nz', 'thewellnz.org', 'www.cdhb.health.nz', 'www.ultimatecare.co.nz',
               'ashleyandmartin.co.nz', 'www.macnz.org', 'www.artscentre.org.nz', 'chchhamradio.org.nz',
               'archives.govt.nz', 'www.k9natural.com', 'www.herculesgazebo.co.nz', 'www.smartcatsstayhome.co.nz',
               'www.livingreef.co.nz', 'www.furtography.co.nz', 'theyardchch.nz', 'riverside.nz', 'm.facebook.com',
               'www.shanghaistreetdumplings.co.nz', 'www.chc.org.nz', 'www.karajoz.co.nz', 'www.nightnday.co.nz',
               'theshelteronline.com', 'www.valleyroad.org.nz', 'www.stbarnabasmounteden.info', 'www.greyfriars.org.nz',
               'www.emmanuelharvestchurch.com', 'lifenz.org', 'lifenz.org', 'epsombaptistchurch.org.nz',
               'quaker.org.nz', 'www.nabc.org.nz', 'www.stgeorgesepsom.org.nz', 'www.saintalbans.org.nz',
               'www.saibabatemple.org.nz', 'www.laparoscopyak.co.nz', 'www.orthoclinic.co.nz',
               'www.cairnhill-healthcentre.co.nz', 'ahns.co.nz', 'www.entgroup.co.nz',
               'www.aucklandradiationoncology.co.nz', 'www.kamranzargar.co.nz', 'www.mercybreastclinic.co.nz',
               'www.healthpoint.co.nz', 'almanar.co.nz', 'www.masjidutsman.org.nz', 'www.aucklandtram.co.nz',
               'www.ipetstore.co.nz', 'www.moona.store', 'aqua-forest-aquarium-studio.business.site', 'wedeliver.nz',
               'www.lifeofriley.co.nz', 'www.brodies.nz', 'www.freerangechef.co.nz', 'www.theseafoodcollective.co.nz',
               'www.dominioneatery.co.nz', 'www.bethshalom.org.nz', 'ahc.org.nz', 'chabad.nz', 'www.bp.com',
               'www.villaridge.co.nz', 'acktauranga.nz', 'www.presbyterian.org.nz', 'www.equipperschurch.com',
               'www.methodist.org.nz', 'www.tcbc.org.nz', 'curatechurch.com', 'www.taurangaelim.nz', 'www.mormon.org',
               'lifezone.church', 'www.lifechurchtga.org.nz', 'www.taurangachurch.org', 'www.salvationarmy.org.nz',
               'abundantlife.org.nz', 'www.stgeorgesgatepa.com', 'www.redeemerchurch.org.nz',
               'sanatandharammandir.org.nz', 'www.ultimatecare.co.nz', 'www.canopycancercare.co.nz',
               'heritagelifecare.co.nz', 'www.chadhealth.co.nz', 'www.healthpoint.co.nz', 'www.thedoctors.co.nz',
               'www.taurangaeyespecialists.co.nz', 'www.thedoctors.co.nz', 'www.tankjuice.co.nz', 'www.tankjuice.co.nz',
               'www.plutojuicebar.com', 'www.downtowntauranga.co.nz', 'www.missgees.co.nz',
               'www.ashburtonbaptist.co.nz', 'jw.org', 'www.methodist.org.nz', 'chchcatholic.nz', 'catholic.org.nz',
               'www.stpaulsashburton.com', 'www.ashburtonnewlife.co.nz', 'www.gracepresbyterianchurch.org.nz',
               'vbcofashburton-nz.org', 'www.anglican.org.nz', 'www.stdavidsashburton.org', 'www.mormon.org',
               'www.terraceview.co.nz', 'heritagelifecare.co.nz', 'www.cdhb.health.nz', 'heritagelifecare.co.nz',
               'www.simplypetfoods.co.nz', 'facebook.com', 'www.chipshop.co.nz', 'www.stpeters.co.nz',
               'www.wakatipuchurch.com', 'www.arrowtown.com', 'www.thestitchingpost.co.nz']

    results = []
    for website in websites:

        print("website " + website)
        result = execute_traceroute_command(website)
        if result is not None:
            results += result

    print(results)







