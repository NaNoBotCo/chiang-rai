# -*- coding: utf-8 -*-
"""content.py — every word on the site, English and Thai, in one place.

Thai is written in the rao/jao register (เฮา · เจ้า · เน้อ · แอ่ว · ม่วน · ยามแลง) over plain
Thai. Prices are Laila Group's own, read from slowboatthailandlaos.com on 2026-09-26.
"""

READ = "26 September 2026"
SHOP = "https://slowboatthailandlaos.com"
TRIP = SHOP + "/trip/"
VISA = "https://www.visaservicesthailand.com/"
DESK = "https://chiangmaivisadesk.com/"
WA = "https://wa.me/66847399996"
PHONE = "+66 84 739 9996"
MAIL = "laila.thailand.travel@gmail.com"
FB = "https://www.facebook.com/Lailahostel/"
IG = "https://www.instagram.com/lailagroup_company/"
OFFICE = (19.9060587, 99.8324613)
ADDRESS = "869/51 Thai Viwat Alley, Wiang, Mueang Chiang Rai 57000"
ADDRESS_TH = "869/51 ซอยไทยวิวัฒน์ ต.เวียง อ.เมืองเชียงราย 57000"

QUOTE_GT = ("One of the most beautiful places in Thailand. It was the highlight of our "
            "visit, and we went back several times.")
QUOTE_TOWN = "Sleepy little town full of lovely people."
QUOTE_OPIUM = ("I highly highly highly recommend visiting both opium museums AND their delightful "
               "giftshops.")

STAY = dict(name="Baan Kan", th="บ้านกาญจน์ เชียงราย", img="own:baan-kan-garden",
            address="254/13 Moo 21, Kaoloi Road, Chiang Rai", phone="+66 80 745 7583",
            book="https://book-directonline.com/properties/baankanchiangraidirect",
            mail="baankan.cei@gmail.com", fb="https://www.facebook.com/102533999501798",
            lat=19.914586, lng=99.835274,
            line="Where NaN stays: a garden guesthouse on Kaoloi Road, a short ride from the clock tower. Tell them NaN sent you.",
            th_line="นอนบ้านกาญจน์ บอกเขาว่า NaN แนะนำมาเน้อเจ้า")


def wa(text: str) -> str:
    import urllib.parse
    return WA + "?text=" + urllib.parse.quote(text)


# ---------------------------------------------------------------- the headline sights
# img: "own:<slug>" (Nan's roll) or "c:<slug>" (Commons). osm: a search that lands on it.
SIGHTS = [
 dict(id="white-temple", name="The White Temple", th="วัดร่องขุ่น", img="own:white-bridge",
      band="c:white-temple-1", osm="Wat Rong Khun",
      kicker="Wat Rong Khun",
      text="Chalermchai Kositpipat, a Chiang Rai son, began rebuilding his home temple in 1997 and "
           "has not stopped. The white stands for the Buddha's purity; the mirror glass set into "
           "every surface is his wisdom, shining out. Arrive early and the whole thing glows.",
      th_text="วัดขาวงามจับใจ๋ ฝีมืออาจารย์เฉลิมชัย ลูกหลานเชียงรายแต๊ ๆ ไปแต่เช้าเน้อเจ้า แสงงามที่สุด",
      laila="one-day-sightseeing-tour-in-chiang-rai"),
 dict(id="blue-temple", name="The Blue Temple", th="วัดร่องเสือเต้น", img="own:blue-temple",
      band="c:blue-temple-1", osm="Wat Rong Suea Ten",
      kicker="Wat Rong Suea Ten",
      text="The Temple of the Dancing Tiger, by the artist Phuttha Kabkaew, one of Chalermchai's "
           "students. Sapphire and gold inside and out, with a white Buddha seated in a room the "
           "colour of deep water. Ten minutes from the clock tower.",
      th_text="วัดสีฟ้าสดใส ข้างในมีพระพุทธรูปสีขาว งามขนาด อยู่ใกล้ตัวเมืองเจ้า",
      laila="one-day-sightseeing-tour-in-chiang-rai"),
 dict(id="black-house", name="The Black House", th="บ้านดำ", img="own:black-house",
      band="c:black-house-1", osm="Baan Dam Museum",
      kicker="Baan Dam",
      text="The painter Thawan Duchanee spent decades building some forty dark teak halls in a "
           "garden north of town and filling them with carved wood, long tables and the things "
           "he loved. Walk slowly; every roofline is its own sculpture.",
      th_text="บ้านดำของอาจารย์ถวัลย์ ดัชนี เรือนไม้สักสีดำกว่าสี่สิบหลัง ในสวนร่มรื่น เดินแอ่วช้า ๆ เน้อ",
      laila="one-day-sightseeing-tour-in-chiang-rai"),
 dict(id="clock-tower", name="The Golden Clock Tower", th="หอนาฬิกาเชียงราย", img="own:clock-gold",
      band="c:clock-tower-2", osm="Chiang Rai Clock Tower", video="v/clock-tower.mp4",
      kicker="Ho Nalika",
      text="Also Chalermchai's, and the heart of the old town. Every evening it runs through its "
           "colours to music: red, green, gold. The night bazaar is a short stroll away, and so "
           "is Laila Group's office on Thai Viwat Alley.",
      th_text="ยามค่ำหอนาฬิกาเปลี่ยนสีตามเสียงเพลง แดง เขียว ทอง ม่วนใจ๋แต๊เจ้า"),
 dict(id="golden-triangle", name="The Golden Triangle", th="สามเหลี่ยมทองคำ", img="own:nan-golden-triangle",
      band="c:golden-triangle-3", osm="Golden Triangle Sop Ruak", href="golden-triangle/",
      kicker="Sop Ruak · the highlight",
      text="Where the Ruak runs into the Mekong and Thailand, Laos and Myanmar meet at one bend "
           "of the river. The most beautiful afternoon in the north. It has its own page.",
      th_text="ตรงที่น้ำรวกบรรจบน้ำโขง สามประเทศมาพบกัน ยามแลงงามที่สุดในภาคเหนือเจ้า",
      laila="one-day-sightseeing-tour-in-chiang-rai"),
 dict(id="phra-kaew", name="Wat Phra Kaew", th="วัดพระแก้ว", img="c:chiang-rai-city-1",
      osm="Wat Phra Kaew Chiang Rai",
      kicker="Where the Emerald Buddha was found",
      text="In 1434 lightning opened a chedi here and revealed the image that became Thailand's "
           "Emerald Buddha. A quiet, green compound in the middle of town, with a jade copy in "
           "a Lanna hall.",
      th_text="วัดที่พบพระแก้วมรกตครั้งแรก เงียบสงบ ร่มเย็น กลางเมืองเจ้า"),
 dict(id="huay-pla-kang", name="Wat Huay Pla Kang", th="วัดห้วยปลากั้ง", img="c:huay-pla-kang-1",
      osm="Wat Huay Pla Kang",
      kicker="The great white Guanyin",
      text="A nine-tiered pagoda and a white Guanyin rising over the trees. "
           "You can ride up inside her and look out over the valley.",
      th_text="เจ้าแม่กวนอิมองค์ใหญ่สีขาว ขึ้นไปชมวิวในองค์ท่านได้เจ้า"),
 dict(id="doi-tung", name="Doi Tung", th="ดอยตุง", img="c:doi-tung-1", osm="Mae Fah Luang Garden",
      kicker="The Princess Mother's mountain",
      text="Terraced flower gardens, the Royal Villa, coffee grown on the slopes around it, and "
           "cool air all year. Laila Group runs it as a private day by car, lunch included.",
      th_text="สวนแม่ฟ้าหลวง พระตำหนัก กาแฟดอยตุง อากาศเย็นสบายตลอดปีเจ้า",
      laila="doi-tung-chiang-rai"),
 dict(id="mae-salong", name="Doi Mae Salong", th="ดอยแม่สลอง", img="c:choui-fong-1", osm="Mae Salong",
      kicker="Tea on the ridgeline",
      text="A Yunnanese hill town among tea terraces. Oolong tastings, noodle shops, and in "
           "January a haze of pink cherry blossom along the road.",
      th_text="ไร่ชาบนดอย ชิมชาอูหลง กิ๋นหมั่นโถว ช่วงหนาวดอกพญาเสือโคร่งบานเต็มดอยเจ้า",
      laila="doi-mae-salong-beautiful-mountain"),
 dict(id="phu-chi-fa", name="Phu Chi Fa", th="ภูชี้ฟ้า", img="c:phu-chi-fa-1", band="c:phu-chi-fa-3",
      osm="Phu Chi Fa",
      kicker="Sunrise over a sea of mist",
      text="A cliff that points at the sky above a valley of cloud. Laila Group's car leaves at "
           "three in the morning so you are standing at the edge when the light comes.",
      th_text="ทะเลหมอกยามเช้า รถออกตีสาม ไปถึงทันแสงแรกเจ้า",
      laila="phu-chi-fa-chiang-rai-mountains"),
 dict(id="tham-luang", name="Tham Luang", th="ถ้ำหลวงขุนน้ำนางนอน", img="own:tham-luang",
      osm="Tham Luang Khun Nam Nang Non", kicker="The Sleeping Lady",
      text="The great cave under Doi Nang Non, the mountain shaped like a woman asleep. The world "
           "knows it from 2018, when all thirteen came home. Today it is a cool, lit, green forest "
           "park with a walk to the cave mouth.",
      th_text="ถ้ำหลวงใต้ดอยนางนอน ปี 2561 ทั้งสิบสามคนกลับบ้านครบ ทุกวันนี้เป็นอุทยานร่มรื่นเจ้า"),
 dict(id="singha-park", name="Singha Park", th="สิงห์ปาร์ค", img="c:singha-park-1", osm="Singha Park Chiang Rai",
      kicker="Tea, lakes and a golden singha",
      text="Rolling tea fields and lakes west of town, good for a bicycle and a long lunch. In "
           "February the balloon fiesta fills the sky.",
      th_text="ไร่ชา ทะเลสาบ ปั่นจักรยาน เดือนกุมภาฯ มีเทศกาลบอลลูนเจ้า"),
]

# ---------------------------------------------------------------- the Golden Triangle page
GT = [
 dict(name="Sop Ruak", th="สบรวก", img="c:golden-triangle-2",
      text="The village at the confluence. Stand on the viewing terrace and the three countries sit "
           "in front of you across the water: Myanmar up the Ruak, Laos across the Mekong."),
 dict(name="The Golden Buddha", th="พระพุทธนวล้านตื้อ", img="c:golden-buddha-1", osm="Golden Triangle Buddha",
      text="A seated golden Buddha on a ship-shaped platform at the water's edge, the landmark of "
           "the bend. Go late in the afternoon, when the gold and the river match."),
 dict(name="The Hall of Opium", th="หอฝิ่น", img="own:opium-mural", osm="Hall of Opium",
      text="The great museum of the valley's history, run by the Mae Fah Luang Foundation, in the "
           "park above Sop Ruak. The painted panels of the farming year are worth the visit on their "
           "own. Leave time for the gift shop."),
 dict(name="The House of Opium", th="บ้านฝิ่น", img="c:mekong-1", osm="House of Opium Sop Ruak",
      text="The small one, in Sop Ruak village: a private museum opened in 1989 by Patcharee "
           "Srimattayakul, born in Chiang Saen. Scales, weights, pipes and the stories behind them, "
           "and a gift shop of its own. Open early to late."),
 dict(name="Coffee and crafts, from the makers", th="กาแฟดอย · งานฝีมือชาวเขา", img="own:across-mekong",
      text="Along the river road and up at the viewpoints, hill-village families sell their own coffee "
           "and their own weaving and embroidery, with the confluence below you."),
 dict(name="The glass walkway", th="สกายวอล์ค", img="own:skywalk",
      text="South of Chiang Saen a glass floor reaches out over the treetops toward the Mekong, "
           "with blossom trees and an arch of flowers at the end. The late sun there is gold."),
 dict(name="Chiang Saen", th="เชียงแสน", img="c:chiang-saen-2", osm="Wat Pa Sak Chiang Saen",
      text="The old Lanna river city, with its brick walls and moat still standing among the trees. "
           "Wat Pa Sak, from 1295, sits in a teak grove on the western edge."),
 dict(name="A longtail on the Mekong", th="ล่องเรือแม่น้ำโขง", img="c:mekong-3",
      text="Boats leave from the landings at Sop Ruak for a loop of the three banks. Twenty minutes "
           "on the water is the best view of the triangle there is."),
]

# ---------------------------------------------------------------- sidequests
SIDE = [
 dict(name="Vanali Vanilla Farm", th="ฟาร์มวานิลลา", img="own:vanilla", osm="Vanali Vanilla Farm",
      text="Vanilla vines under shade cloth, on the edge of town. The farm shows its flowers "
           "and sells its pods."),
 dict(name="The bus-station pillars", th="เสาภาพวาดสถานีขนส่ง", img="own:mural-friends",
      text="Every pillar at the city bus station by the night bazaar is painted as a window onto "
           "somewhere in the province: tea hills, the golden naga, two friends on a bus. Go at "
           "seven in the morning with a coffee."),
 dict(name="The hamsa of Thai Viwat", th="หงส์ทองซอยไทยวิวัฒน์", img="own:hamsa",
      text="A gilded hamsa, the swan of Lanna temples, round the corner from Laila Group's office. "
           "Say hello on your way to book."),
 dict(name="Evening guardians", th="ยักษ์ยามค่ำ", img="own:yak",
      text="After dark the temple guardians near the night bazaar are lit violet and gold. A good "
           "walk after khao soi."),
 dict(name="Chiang Rai Youth Orchestra", th="วงออร์เคสตราเยาวชนเชียงราย", img="own:orchestra",
      text="Violin, viola, cello, double bass and ukulele, taught to the city's children. If they are playing while you are in town, go."),
 dict(name="Hot-spring eggs at Mae Kachan", th="ต้มไข่บ่อน้ำร้อนแม่ขะจาน", img="c:mae-kachan-1",
      osm="Mae Kachan hot spring",
      text="On the road south, a geyser, a row of stalls and baskets of eggs to lower into the "
           "spring. A few minutes later, breakfast."),
 dict(name="The warm waterfall at Phu Sang", th="น้ำตกภูซาง", img="c:phu-sang-1", osm="Phu Sang Waterfall",
      text="A waterfall that runs warm, over orange stone, in a national park toward Phayao. You "
           "can stand under it."),
 dict(name="The Kok River", th="แม่น้ำกก", img="c:kok-river-2", osm="Kok River Chiang Rai",
      text="The river that runs through town. Sand beaches in the dry months, longtail boats "
           "upstream toward the hill villages."),
 dict(name="Khao soi, twice a day", th="ข้าวซอย", img="c:khao-soi-2",
      text="Curry noodles with a crisp nest on top, pickled greens and shallots on the side. The "
           "north's own breakfast, lunch and consolation."),
 dict(name="The night bazaar", th="ไนท์บาซาร์", img="c:night-bazaar-1", osm="Chiang Rai Night Bazaar",
      text="A food court under the stars with a stage for dancers, two minutes from the bus "
           "station. On Saturdays the walking street on Thanalai Road goes on for blocks."),
 dict(name="Morning coffee", th="กาแฟยามเช้า", img="own:coffee",
      text="Chiang Rai grows its own coffee on Doi Chang and Doi Tung, and the cafés in town pour "
           "it every way you can think of. Laila Group runs a whole day up Doi Chang.",
      laila="doi-chang-coffee-mountain-tour"),
 dict(name="The Hall of Opium murals", th="ภาพเขียนหอฝิ่น", img="own:opium-mural-2",
      text="A second look: the panels follow a hill family through the year, from sharpening the "
           "tools in March to the harvest in January."),
]

# ---------------------------------------------------------------- Laila Group, from her own pages
BOATS = [
 dict(name="Slow boat to Luang Prabang", th="เรือช้าไปหลวงพระบาง", days="2 days, 1 night", price=1690,
      slug="slow-boat-chiang-rai-to-luang-prabang",
      text="Pickup at 05:00 from your hotel or Sofia Hostel, the border by eight, the boat at ten, "
           "Pak Beng by five. Day two leaves at nine and lands in Luang Prabang at four. Border "
           "bus, pier taxi, boat ticket and a day-one lunch box included."),
 dict(name="Slow boat, the gentle version", th="เรือช้า สามวันสองคืน", days="3 days, 2 nights", price=2340,
      slug="slow-boat-chiang-rai-to-luang-prabang-b",
      text="A midday pickup, a first night in a Huay Xai hotel (included), then two unhurried days "
           "on the river by way of Pak Beng."),
 dict(name="Slow boat to Pak Beng", th="เรือช้าไปปากแบ่ง", days="1 day", price=1450,
      slug="chiang-rai-to-pak-beng-slow-boat",
      text="One long, lovely day on the Mekong, with a stop at the Huay Xai office for a Lao SIM "
           "and kip on the way."),
 dict(name="From Chiang Mai, by slow boat", th="จากเชียงใหม่ ล่องเรือช้า", days="3 days, 2 nights", price=2890,
      slug="chiang-mai-to-luang-prabang",
      text="Pickup in Chiang Mai at nine, a stop at the White Temple, the night in Huay Xai, then "
           "the river. Travel insurance included."),
]
TRAINS = [
 ("Train to Luang Prabang, in a day", "train-to-luang-prabang", 1890),
 ("Train to Vang Vieng", "train-to-vang-viang", 2290),
 ("Train to Vientiane", "train-to-vientiane", 2390),
 ("Sleeper bus to Luang Prabang", "chiang-rai-to-luang-prabang-sleeper-bus", 1990),
 ("Chiang Mai to Luang Prabang by train", "chiang-mai-to-luang-prabang-by-train", 2990),
 ("Luang Prabang back to Chiang Rai", "train-from-luang-prabang-to-chiang-rai-thailand", 2190),
]
DAYS = [
 ("One day, all of it", "one-day-sightseeing-tour-in-chiang-rai", "฿1,200 a person",
  "White Temple, Blue Temple, Black House, the Long Neck village, a tea plantation, the Golden "
  "Triangle and the Hall of Opium. Guide, buffet lunch and water; 08:00 to 18:00."),
 ("Doi Tung", "doi-tung-chiang-rai", "฿3,500 a car, up to three",
  "Palace, market, flower garden, museum, temple and lunch."),
 ("Doi Mae Salong", "doi-mae-salong-beautiful-mountain", "฿3,500 a car, up to three",
  "Tea terraces and the Yunnanese hill town."),
 ("Phu Chi Fa sunrise", "phu-chi-fa-chiang-rai-mountains", "฿3,000 a car, up to three",
  "Leaves at 03:00 for first light over the mist."),
 ("Doi Chang coffee", "doi-chang-coffee-mountain-tour", "฿2,500 a car, up to three",
  "A day among the coffee farms."),
 ("Doi Pha Mee and Pha Hi", "plan-your-amazing-doi-phamee-pha-hi-explore-mountains-coffee",
  "฿3,000 a car, up to three", "Mountain villages and coffee along the border ridge."),
 ("A day of trekking", "one-day-trekking-hiking-adventure", "฿1,500 a person, two or more",
  "With a TAT-certified guide."),
 ("Two days in the hills", "a-day-trekking-nature-and-adventure-package", "฿2,890 a person",
  "A Lisu village night, a Chinese tea village, a waterfall swim, lunch cooked in bamboo, a hot spring."),
 ("A day with elephants", "a-day-with-elephants-nature-care-connection", "฿1,990 half · ฿2,890 full",
  "Feeding, walking and caring for elephants."),
]
WHEELS = [
 ("Honda Scoopy", "honda-scoopy-i-affordable-110cc-scooter", 250),
 ("Honda Click 125", "honda-click-125-reliable-mid-size-scooter", 300),
 ("Honda PCX 160", "honda-pcx-160-premium-scooter-rental", 500),
 ("Toyota Vios, with driver", "toyota-vios-2018-car-rental-with-driver", 1200),
 ("Honda Civic, with driver", "honda-civic-sedan-rental-with-driver", 1200),
 ("Toyota Innova, 7 seats", "toyota-innova-7-seater-family-car", 1500),
 ("Toyota Sienta, 6 seats", "toyota-sienta-6-seater-minivan-rental", 1600),
 ("Toyota Fortuner, 7 seats", "toyota-fortuner-7-seater-suv-rental", 2200),
 ("Toyota Hiace, 10 seats", "toyota-hiace-2011-10-seats-van-rental", 2200),
]
VISAS = [
 ("DTV", "the Destination Thailand Visa"),
 ("Thailand Privilege", "five to twenty years"),
 ("Non-Immigrant O", "retirement or marriage"),
 ("LTR", "the long-term resident visa"),
 ("SMART", "with the pitch prepared for the National Innovation Agency"),
 ("90-day reports and TM.30", "kept on schedule for you"),
 ("A bank account", "at Bangkok Bank or SCB"),
 ("A company and a Non-B", "registration and the visa that follows"),
]

# ---------------------------------------------------------------- margin notes (the native ads)
NOTES = {
 "boat": dict(kicker="Laila Group", th="ล่องเรือช้า",
              line="Two days down the Mekong to Luang Prabang, from ฿1,690, picked up at your door.",
              href="slow-boat/", cta="The slow boat"),
 "day": dict(kicker="Laila Group", th="เที่ยววันเดียว",
             line="White, Blue, Black, and the Golden Triangle by sunset: one day, ฿1,200, lunch included.",
             href=TRIP + "one-day-sightseeing-tour-in-chiang-rai/", cta="Book the day"),
 "car": dict(kicker="Laila Group", th="รถพร้อมคนขับ",
             line="A car and driver from ฿1,200 a day. A Scoopy from ฿250.",
             href="with-laila/#wheels", cta="Wheels"),
 "visa": dict(kicker="Visa Services Thailand", th="วีซ่า",
              line="Staying the season? Laila's visa office is on the same alley.",
              href="with-laila/#visas", cta="Visas"),
 "desk": dict(kicker="Chiang Mai Visa Desk", th="เชียงใหม่",
              line="Going on to Chiang Mai? The visa desk there speaks Thai and English, and does America too.",
              href=DESK, cta="chiangmaivisadesk.com", ext=True),
 "shop": dict(kicker="Laila's Designer Consignment", th="ร้านแบรนด์เนมฝากขาย",
              line="Designer pieces, consigned, next door to the visa office.",
              href="with-laila/#shop", cta="The shop"),
 "wa": dict(kicker="Laila Group", th="ทักมาเน้อ",
            line="Ask anything on WhatsApp, in English or Thai.",  # stylecheck: allow — call to action
            href=wa("Hello Laila Group! I found you on Chiang Rai, Slowly."), cta=PHONE, ext=True),
}

# ---------------------------------------------------------------- lanterns: Yi Peng & Loy Krathong
# Night from the Thai calendar listings for 2026; the 2025 Chiang Rai events are from
# chiangraicity.go.th (news 31989, 32000) and chiangrai.prd.go.th (content 236860).
LANTERN_NIGHT = "2026-11-24"
LANTERNS = [
 dict(name="The Kok River", th="ริมน้ำกก · วัดฝั่งหมิ่น", img="c:kok-river-2", osm="Wat Fang Min",
      line="A giant krathong on the river, then sa-pao boats of light drift downstream.",
      th_line="กระทงใหญ่กลางน้ำกก แล้วล่องสะเปาเจ้า"),
 dict(name="Chiang Saen", th="ลอยกระทง 4 ชาติ", img="c:lantern-candles", osm="Chiang Saen",
      line="Four nations float together by the Golden Triangle: a thousand lamps on the Mekong.",
      th_line="ไทย ลาว เมียนมา จีน ลอยกระทงร่วมกัน ประทีปล้านดวงเจ้า"),
 dict(name="Your own", th="กระทงใบตอง", img="c:krathong-float",
      line="Banana leaf, a candle, three incense sticks, a wish. Let it go.",
      th_line="ใบตอง เทียน ธูปสามดอก อธิษฐาน แล้วปล่อยไปเน้อ"),
]
NOTES["lantern"] = dict(kicker="Laila Group", th="คืนยี่เป็ง",
    line="A car and driver to Chiang Saen for lantern night, and back to town after.",
    href=wa("Hello Laila Group! A car to Chiang Saen for Loy Krathong night, please."), cta="Ask Laila", ext=True)
