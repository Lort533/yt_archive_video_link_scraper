import json, time, urllib.request, re

link_list = json.load(open('link_list.json')) # Origin: https://web.archive.org/web/timemap/json?url=http%3A%2F%2Fwww.youtube.com%2Fwatch.php%3Fv%3D&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..&limit=10000&_=1792873540935
link_list.remove(link_list[0])

target_links = {}
date_cap = input("Please input your date cap (inclusive, e.g.: 2006, 200511 or 20060213): ")
for link in link_list:
    if int(link[2][:len(date_cap)]) <= int(date_cap):
        if not target_links.get(link[2]):
            target_links[int(link[2])] = []
        target_links[int(link[2])].append(link)

#blocked_links = ["http://www.myspace.com/"]

found_links = json.load(open('scraped_links.json'))
rate_limit = int(input("Please input your rate limit in seconds (0 for none): "))
for link in sorted(target_links):
    for link in target_links[link]:
        print("Now processing " + link[2] + " for " + link[0])
        
        with urllib.request.urlopen("https://web.archive.org/web/" + link[2] + "id_/" + link[0]) as response:
            response = response.read().decode('utf-8')
            found_links.extend(re.findall('<b>\\d+ clicks from </b> <a href="[^"]+">(.+)</a><br>', response))
        found_links.extend(re.findall('<span class="label">\\d+ clicks from</span> <a.+href="([^"]+)".+>.+</a>', response))
        
        time.sleep(rate_limit)

# Examples for regex testing:
#
#for link in ["https://web.archive.org/web/20051102085540/http://www.youtube.com:80/watch.php?v=4Q9dw02whKs", "https://web.archive.org/web/20060907044333/http://www.youtube.com/watch.php?v=62msXSpu6-c", "https://web.archive.org/web/20061201023649/http://www.youtube.com/watch.php?v=zA3FbY_0VqY"]:
#    with urllib.request.urlopen(link) as response:
#        response = response.read().decode('utf-8')
#        found_links.extend(re.findall('<b>\\d+ clicks from </b> <a href="[^"]+">(.+)</a><br>', response))
#        found_links.extend(re.findall('<span class="label">\\d+ clicks from</span> <a.+href="([^"]+)".+>.+</a>', response))
#    time.sleep(rate_limit)

with open('scraped_links.json', 'w') as file:
    json.dump(found_links, file)

print("New link list:")
for link in found_links:
    print(link)
