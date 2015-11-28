import urllib, urllib2
import json
import httplib2

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.context_processors import csrf
from django.views import generic

from models import PurchaseHistory
from forms import PurchaseHistoryForm

import logging
log = logging.getLogger(__name__)


def index(request):
    #Check session for returning customer
    user = checkReturningCustomer(request)
    '''
    url = "https://careers.undercovertourist.com/assignment/1/products/"
    products = getProduct(url)['results']
    '''
    productsDict = {
            "count": 100,
            "results": [
                {
                    "slug": "3-day-magic-your-way",
                    "id": 101,
                    "name": "3-Day Magic Your Way",
                    "uuid": "448b8e28-225b-4526-871b-8c5333e137af"
                },
                {
                    "slug": "3-day-park-hopper",
                    "id": 102,
                    "name": "3-Day Park Hopper?",
                    "uuid": "058803c7-a54e-4d4d-bbba-b0e6b27a1852"
                },
                {
                    "slug": "4-day-magic-your-way",
                    "id": 103,
                    "name": "4-Day Magic Your Way",
                    "uuid": "59600868-2d71-4b00-8e7f-edb45a947600"
                },
                {
                    "slug": "5-day-magic-your-way",
                    "id": 104,
                    "name": "5-Day Magic Your Way",
                    "uuid": "9c2c783d-32eb-4313-8330-2d63506db7c7"
                },
                {
                    "slug": "10-day-magic-your-way",
                    "id": 105,
                    "name": "10-Day Magic Your Way",
                    "uuid": "1dd1ebc6-49d5-4823-b87b-80d308ed4d8a"
                },
                {
                    "slug": "10-day-park-hopper",
                    "id": 106,
                    "name": "10-Day Park Hopper?",
                    "uuid": "4e902117-f0a4-4850-9cca-a81725367e70"
                },
                {
                    "slug": "10-day-park-hopper-no-expiration",
                    "id": 107,
                    "name": "10-Day Park Hopper? - No Expiration",
                    "uuid": "ed98a667-0d72-47f8-af4e-7918e722c546"
                },
                {
                    "slug": "4-day-water-park-fun-more",
                    "id": 108,
                    "name": "4-Day Water Park Fun & More",
                    "uuid": "c2759118-756b-42d5-8467-824c4ae76624"
                },
                {
                    "slug": "4-day-park-hopper-water-park-fun-more",
                    "id": 109,
                    "name": "4-Day Park Hopper? + Water Park Fun & More",
                    "uuid": "541faf92-2688-4718-9842-2336a8540cda"
                },
                {
                    "slug": "1-day-disneys-blizzard-beach-or-disneys-typhoon-lagoon-water-parks",
                    "id": 110,
                    "name": "1-Day Disney?s Blizzard Beach or Disney?s Typhoon Lagoon Water Parks",
                    "uuid": "af727a28-fc0a-4cd1-8db7-209ddf3f8c6e"
                },
                {
                    "slug": "1-day-disneyquest-indoor-interactive-theme-park",
                    "id": 111,
                    "name": "1-Day DisneyQuest? Indoor Interactive Theme Park",
                    "uuid": "b6f7782e-2767-4df4-be21-7b37470e9f61"
                },
                {
                    "slug": "1-day-magic-your-way",
                    "id": 112,
                    "name": "1-Day Magic Your Way (Epcot or Studios or AK)",
                    "uuid": "323b2db9-6452-40a0-b866-fc93c162917d"
                },
                {
                    "slug": "2-day-magic-your-way",
                    "id": 113,
                    "name": "2-Day Magic Your Way",
                    "uuid": "62a68423-c72a-49f0-a2d1-431628757094"
                },
                {
                    "slug": "1-day-magic-your-way-magic-kingdom-park",
                    "id": 114,
                    "name": "1-Day Magic Your Way (Magic Kingdom? Park)",
                    "uuid": "402e4d0e-ca50-401a-84cd-ef4e95041193"
                },
                {
                    "slug": "1-day-park-hopper",
                    "id": 115,
                    "name": "1-Day Park Hopper?",
                    "uuid": "c95100ea-ed97-4529-8eb4-8c5b304c37a7"
                },
                {
                    "slug": "2-day-park-hopper",
                    "id": 116,
                    "name": "2-Day Park Hopper?",
                    "uuid": "8088c883-face-483e-9ada-3ba96c9434d2"
                },
                {
                    "slug": "5-day-magic-your-way-no-expiration",
                    "id": 117,
                    "name": "5-Day Magic Your Way - No Expiration",
                    "uuid": "c5f2ae89-9835-4d78-a7d5-a30ccf7b9d66"
                },
                {
                    "slug": "10-day-magic-your-way-no-expiration",
                    "id": 118,
                    "name": "10-Day Magic Your Way - No Expiration",
                    "uuid": "512783fc-35f4-4990-91b7-c8dcf9e4e7b9"
                },
                {
                    "slug": "10-day-water-park-fun-more",
                    "id": 119,
                    "name": "10-Day Water Park Fun & More",
                    "uuid": "001d5dbe-b742-4eea-889d-18e45b0683d2"
                },
                {
                    "slug": "10-day-water-park-fun-more-no-expiration",
                    "id": 120,
                    "name": "10-Day Water Park Fun & More - No Expiration",
                    "uuid": "6d8f5a25-02ac-4784-9a89-425a494a4ad7"
                },
                {
                    "slug": "10-day-park-hopper-water-park-fun-more",
                    "id": 121,
                    "name": "10-Day Park Hopper? + Water Park Fun & More",
                    "uuid": "b003305c-69b0-428f-840c-4dcb9943d3d1"
                },
                {
                    "slug": "10-day-park-hopper-water-park-fun-more-no-expiration",
                    "id": 122,
                    "name": "10-Day Park Hopper? + Water Park Fun & More - No Expiration",
                    "uuid": "72ea3c29-9fd3-48f2-a398-0b510407f350"
                },
                {
                    "slug": "1-day-universal-base",
                    "id": 123,
                    "name": "1-Day Universal Base Ticket",
                    "uuid": "707fa7c6-7963-435b-b058-e94a0acc8ba5"
                },
                {
                    "slug": "2-day-universal-base",
                    "id": 124,
                    "name": "2-Day Universal Base Ticket",
                    "uuid": "7d4266ae-db0a-47f4-89e2-224a6a1dcae5"
                },
                {
                    "slug": "3-day-universal-base",
                    "id": 125,
                    "name": "3-Day Universal Base Ticket",
                    "uuid": "57961e60-247f-4bf5-b062-b673b0097b12"
                },
                {
                    "slug": "4-day-universal-base",
                    "id": 126,
                    "name": "4-Day Universal Base Ticket",
                    "uuid": "17621d01-5bb2-4430-a575-d4dac6022ca5"
                },
                {
                    "slug": "1-day-universal-park-to-park",
                    "id": 127,
                    "name": "1-Day Universal Park-to-Park Ticket",
                    "uuid": "85b1db0b-c9e6-419a-bfd7-651a129d0b3a"
                },
                {
                    "slug": "2-day-universal-park-to-park",
                    "id": 128,
                    "name": "2-Day Universal Park-to-Park Ticket",
                    "uuid": "943e606b-002e-4057-b2da-b4068ac0e447"
                },
                {
                    "slug": "3-day-universal-park-to-park",
                    "id": 129,
                    "name": "3-Day Universal Park-to-Park Ticket",
                    "uuid": "3e03f63b-6e99-4ed9-a9fd-03ce89cdee37"
                },
                {
                    "slug": "4-day-universal-park-to-park",
                    "id": 130,
                    "name": "4-Day Universal Park-to-Park Ticket",
                    "uuid": "3eb82e84-c04e-4ce6-a064-c037364636a3"
                },
                {
                    "slug": "3-park-unlimited-universal",
                    "id": 131,
                    "name": "3-Park Unlimited Universal Ticket",
                    "uuid": "b11243c8-5807-4970-b3bf-61b5dfb020e9"
                },
                {
                    "slug": "2014-wet-n-wild-length-of-stay",
                    "id": 132,
                    "name": "2014 Wet 'n Wild Length of Stay Ticket ",
                    "uuid": "afdab503-9500-4515-a029-95c7eca80cda"
                },
                {
                    "slug": "1-day-gatorland",
                    "id": 133,
                    "name": "1-Day Gatorland Ticket",
                    "uuid": "e2ea01de-42e5-44a5-ba19-b57d0a761e4f"
                },
                {
                    "slug": "2014-ripleys-believe-it-or-not",
                    "id": 134,
                    "name": "2014 Ripley's Believe It or Not! Ticket",
                    "uuid": "a4dccd3c-2a18-4763-b18a-46e215662f7a"
                },
                {
                    "slug": "knotts-berry-farm-single-day",
                    "id": 135,
                    "name": "2014 Knott's Berry Farm Single Day Ticket",
                    "uuid": "8899999a-ed66-4df6-b1a0-a75f0ed359d3"
                },
                {
                    "slug": "2015-knotts-soak-city-oc-single-day",
                    "id": 136,
                    "name": "2015 Knott's Soak City OC Single Day Ticket",
                    "uuid": "a7b4c1c8-cf41-47a9-a497-522bd48a5b1c"
                },
                {
                    "slug": "2014-knotts-berry-farm-ride-slide-single-day-combo",
                    "id": 137,
                    "name": "2014 Knott's Berry Farm Ride & Slide Single Day Combo Ticket",
                    "uuid": "7d4be997-db32-4f8e-9b0c-9e9239abfc6b"
                },
                {
                    "slug": "legoland-california",
                    "id": 138,
                    "name": "2014 LEGOLAND California Ticket",
                    "uuid": "68e8059f-a950-4def-8f49-74ee0d60c132"
                },
                {
                    "slug": "legoland-california-sea-life-aquarium-hopper-2nd-day-free",
                    "id": 139,
                    "name": "2014 LEGOLAND California & SEA LIFE Aquarium Hopper + 2nd Day FREE",
                    "uuid": "b3c88473-b29c-41ee-9721-528521397d2b"
                },
                {
                    "slug": "legoland-california-resort-hopper-2nd-day-free",
                    "id": 140,
                    "name": "2014 LEGOLAND California Resort Hopper + 2nd Day FREE",
                    "uuid": "9c38ce5c-732d-4e86-8525-2199b193454d"
                },
                {
                    "slug": "2014-six-flags-magic-mountain",
                    "id": 141,
                    "name": "2014 Six Flags Magic Mountain ",
                    "uuid": "6213b432-81dd-4c94-86cb-dc7837bd5cdc"
                },
                {
                    "slug": "2014-fright-fest-six-flags-magic-mountain",
                    "id": 142,
                    "name": "2014 Fright Fest - Six Flags Magic Mountain",
                    "uuid": "efe6e11b-7546-4ef9-a285-10beba7e741d"
                },
                {
                    "slug": "2014-six-flags-hurricane-harbor",
                    "id": 143,
                    "name": "2014 Six Flags Hurricane Harbor",
                    "uuid": "d0d28b04-9ae6-4341-9f5d-04e9a243bf74"
                },
                {
                    "slug": "1-day-uss-midway-museum",
                    "id": 144,
                    "name": "1-Day USS Midway Museum",
                    "uuid": "1eadad4e-0f25-4c7e-85fd-cbef97d5a386"
                },
                {
                    "slug": "2014-universal-studios-hollywood-single-day-pass",
                    "id": 145,
                    "name": "2014 Universal Studios Hollywood Single Day Pass",
                    "uuid": "d7081eb8-917c-477c-bee1-1c9a3a8f9e48"
                },
                {
                    "slug": "2014-universal-studios-hollywood-front-of-the-line-pass-peak",
                    "id": 146,
                    "name": "2014 Universal Studios Hollywood Front of the Line Pass - Peak",
                    "uuid": "12b5ffa0-9614-4859-9949-06d301bc8c41"
                },
                {
                    "slug": "2014-ripleys-believe-it-or-not-hollywood",
                    "id": 147,
                    "name": "2014 Ripley's Believe It or Not! Hollywood Ticket",
                    "uuid": "042283f5-ba79-4842-aad9-4ecb1c0d3d2b"
                },
                {
                    "slug": "2014-madame-tussauds-hollywood",
                    "id": 148,
                    "name": "2014 Madame Tussauds Hollywood All Access Ticket",
                    "uuid": "d8733158-060e-468b-b5e5-b419864757d2"
                },
                {
                    "slug": "24-hour-hop-on-hop-off-double-decker-bus-pass",
                    "id": 149,
                    "name": "24 Hour Hop-On, Hop-Off Double Decker Bus Pass",
                    "uuid": "4d539056-603e-4db5-bc15-e4310bc5746f"
                },
                {
                    "slug": "48-hour-hop-on-hop-off-double-decker-bus-pass",
                    "id": 150,
                    "name": "48 Hour Hop-On, Hop-Off Double Decker Bus Pass",
                    "uuid": "755344c6-c7a0-47f2-8e11-e8b236c34ffd"
                },
                {
                    "slug": "3-day-park-hopper-plus-extra-day-free",
                    "id": 151,
                    "name": "3-Day Park Hopper? - plus extra day free",
                    "uuid": "b9b9fca8-a74b-4911-bae7-cae142f4267c"
                },
                {
                    "slug": "3-day-water-park-fun-more",
                    "id": 152,
                    "name": "3-Day Water Park Fun & More",
                    "uuid": "edb2f9df-f17c-41c4-bac2-5105b733a327"
                },
                {
                    "slug": "2-day-universal-base-ticket-plus-extra-day-free",
                    "id": 153,
                    "name": "2-Day Universal Base Ticket - plus extra day free",
                    "uuid": "29d49a1b-47eb-45bf-bf7e-5db7084aef3c"
                },
                {
                    "slug": "4-day-magic-your-way-plus-extra-day-free",
                    "id": 154,
                    "name": "4-Day Magic Your Way - plus extra day free",
                    "uuid": "b31c9235-7ce4-445b-8e7e-6249ba191908"
                },
                {
                    "slug": "4-day-park-hopper-plus-extra-day-free",
                    "id": 155,
                    "name": "4-Day Park Hopper? - plus extra day free",
                    "uuid": "20fcb272-28a2-4ad1-ac33-a1f90bcf1f6b"
                },
                {
                    "slug": "3-day-water-park-fun-more-plus-extra-day-free",
                    "id": 156,
                    "name": "3-Day Water Park Fun & More - plus extra day free",
                    "uuid": "7456c9ff-d975-47e9-a144-222a6f93ef1f"
                },
                {
                    "slug": "3-day-park-hopper-water-park-fun-more-plus-extra-day-free",
                    "id": 157,
                    "name": "3-Day Park Hopper? + Water Park Fun & More - plus extra day free",
                    "uuid": "8d2c1fd2-0756-4b90-8ab0-eabccfeab708"
                },
                {
                    "slug": "4-day-park-hopper",
                    "id": 158,
                    "name": "4-Day Park Hopper?",
                    "uuid": "d11fd9b7-de90-43df-84f0-18aafeb1a158"
                },
                {
                    "slug": "3-day-park-hopper-water-park-fun-more",
                    "id": 159,
                    "name": "3-Day Park Hopper? + Water Park Fun & More",
                    "uuid": "1d838839-9822-4a45-9836-3327e72c89cd"
                },
                {
                    "slug": "2014-san-diego-zoo-safari-park",
                    "id": 160,
                    "name": "2014 San Diego Zoo Safari Park Ticket",
                    "uuid": "bdd369d9-d7a5-4731-aff0-70215b9bf7b0"
                },
                {
                    "slug": "2014-san-diego-zoo",
                    "id": 161,
                    "name": "2014 San Diego Zoo Ticket",
                    "uuid": "dcb7b256-12bc-4e57-88f5-553dc841e3be"
                },
                {
                    "slug": "2014-universal-studios-hollywood-front-of-the-line-pass-off-peak",
                    "id": 162,
                    "name": "2014 Universal Studios Hollywood Front of the Line Pass - Off-Peak",
                    "uuid": "1f755fdd-c77b-4fef-b6d9-67f491e20c68"
                },
                {
                    "slug": "2014-universal-studios-hollywood-2-day-pass",
                    "id": 163,
                    "name": "2014 Universal Studios Hollywood 2 Day Pass",
                    "uuid": "fc4dd746-08dd-4b04-8a31-7202ed23b7a9"
                },
                {
                    "slug": "2-day-universal-park-to-park-ticket-plus-extra-day-free",
                    "id": 164,
                    "name": "2-Day Universal Park-to-Park Ticket - plus extra day free",
                    "uuid": "43e2efc4-dd3f-11e3-9143-22000a2f94e3"
                },
                {
                    "slug": "2-day-universal-park-to-park-ticket-plus-extra-day-free-promo",
                    "id": 165,
                    "name": "2-Day Universal Park-to-Park Ticket - plus extra day free (PROMO)",
                    "uuid": "8c2f1e62-efaa-4738-b49d-9562afe084ba"
                },
                {
                    "slug": "2015-san-diego-zoo-safari-park",
                    "id": 166,
                    "name": "2015 San Diego Zoo Safari Park Ticket",
                    "uuid": "96f910c9-97a4-4a61-8703-7c89be8ddbb6"
                },
                {
                    "slug": "2015-san-diego-zoo",
                    "id": 167,
                    "name": "2015 San Diego Zoo Ticket",
                    "uuid": "790532ce-3e88-40d7-b5d5-a30af17b48d8"
                },
                {
                    "slug": "2015-universal-studios-hollywood-front-of-the-line-pass-off-peak",
                    "id": 168,
                    "name": "2015 Universal Studios Hollywood Front of the Line Pass - Off-Peak",
                    "uuid": "8e71e048-56dc-4ca9-b776-161c920263c1"
                },
                {
                    "slug": "2015-universal-studios-hollywood-front-of-the-line-pass-peak",
                    "id": 169,
                    "name": "2015 Universal Studios Hollywood Front of the Line Pass - Peak",
                    "uuid": "26f1b0b6-7bb7-4b7e-aa86-1100faf4f789"
                },
                {
                    "slug": "knotts-berry-farm-single-day-",
                    "id": 170,
                    "name": "2015 Knott's Berry Farm Single Day Ticket",
                    "uuid": "ab4d6835-932c-44f2-bd17-ae806b925e0e"
                },
                {
                    "slug": "2015-ripleys-believe-it-or-not",
                    "id": 171,
                    "name": "2015 Ripley's Believe It or Not! Ticket",
                    "uuid": "511f7247-1e02-4919-b833-8ad1eaa029f8"
                },
                {
                    "slug": "2015-legoland-california-sea-life-aquarium-hopper-2nd-day-free",
                    "id": 172,
                    "name": "2015 LEGOLAND California & SEA LIFE Aquarium Hopper + 2nd Day FREE",
                    "uuid": "fc80c52c-db2a-4107-9aff-ce5111f13092"
                },
                {
                    "slug": "2015-legoland-california-resort-hopper-2nd-day-free",
                    "id": 173,
                    "name": "2015 LEGOLAND California Resort Hopper + 2nd Day FREE",
                    "uuid": "3ffd1078-ea57-4f23-82d9-880c9e1e83c9"
                },
                {
                    "slug": "2015-legoland-california",
                    "id": 174,
                    "name": "2015 LEGOLAND California Ticket",
                    "uuid": "c6717508-42fa-4410-ae00-7be774ec261e"
                },
                {
                    "slug": "2015-madame-tussauds-hollywood",
                    "id": 175,
                    "name": "2015 Madame Tussauds Hollywood All Access Ticket",
                    "uuid": "8ea21399-7bd8-43fe-b872-d808f896b923"
                },
                {
                    "slug": "2015-ripleys-believe-it-or-not-hollywood",
                    "id": 176,
                    "name": "2015 Ripley's Believe It or Not! Hollywood Ticket",
                    "uuid": "b2db56e1-8324-4922-8ad1-dfe26b82715a"
                },
                {
                    "slug": "1-day-magic-your-way-e",
                    "id": 177,
                    "name": "1-Day Magic Your Way (Epcot or Studios or AK)  (E-Ticket)",
                    "uuid": "7b18ec2f-c753-4781-a313-498c924d9551"
                },
                {
                    "slug": "1-day-magic-your-way-magic-kingdom-park-e",
                    "id": 178,
                    "name": "1-Day Magic Your Way (Magic Kingdom? Park) (E-Ticket)",
                    "uuid": "b806fd8a-0d1e-404a-a5ed-f804fbc3f6e9"
                },
                {
                    "slug": "1-day-park-hopper-e",
                    "id": 179,
                    "name": "1-Day Park Hopper?  (E-Ticket)",
                    "uuid": "00cec384-1e21-44f7-bc1f-c1028c965e07"
                },
                {
                    "slug": "10-day-magic-your-way-e",
                    "id": 180,
                    "name": "10-Day Magic Your Way (E-Ticket)",
                    "uuid": "552d4c58-2ed7-40da-a67f-3617d5504bb1"
                },
                {
                    "slug": "10-day-magic-your-way-no-expiration-e",
                    "id": 181,
                    "name": "10-Day Magic Your Way - No Expiration (E-Ticket)",
                    "uuid": "8d979835-6825-49bb-967b-5abdb329e4e6"
                },
                {
                    "slug": "10-day-park-hopper-e",
                    "id": 182,
                    "name": "10-Day Park Hopper? (E-Ticket)",
                    "uuid": "6f2c1094-8cae-4d47-aa87-08e93986186b"
                },
                {
                    "slug": "10-day-park-hopper-no-expiration-e",
                    "id": 183,
                    "name": "10-Day Park Hopper? - No Expiration (E-Ticket)",
                    "uuid": "3134a1db-ecda-494c-96f1-339f6e08f4e8"
                },
                {
                    "slug": "10-day-park-hopper-water-park-fun-more-e",
                    "id": 184,
                    "name": "10-Day Park Hopper? + Water Park Fun & More (E-Ticket)",
                    "uuid": "591a010e-28ed-452f-8220-0d0f3a31ee61"
                },
                {
                    "slug": "10-day-park-hopper-water-park-fun-more-no-expiration-e",
                    "id": 185,
                    "name": "10-Day Park Hopper? + Water Park Fun & More - No Expiration (E-Ticket)",
                    "uuid": "4aaf951e-af24-4609-80b7-15b56e4e1fab"
                },
                {
                    "slug": "10-day-water-park-fun-more-e",
                    "id": 186,
                    "name": "10-Day Water Park Fun & More (E-Ticket)",
                    "uuid": "3516723f-666f-47ac-842a-55d12a7d55c6"
                },
                {
                    "slug": "10-day-water-park-fun-more-no-expiration-e",
                    "id": 187,
                    "name": "10-Day Water Park Fun & More - No Expiration (E-Ticket)",
                    "uuid": "dfc9d826-f595-436c-9c29-807a7cf3f930"
                },
                {
                    "slug": "2-day-magic-your-way-e",
                    "id": 188,
                    "name": "2-Day Magic Your Way (E-Ticket)",
                    "uuid": "eed7e76c-f79c-4f14-a601-6576cf1d4921"
                },
                {
                    "slug": "2-day-park-hopper-e",
                    "id": 189,
                    "name": "2-Day Park Hopper? (E-Ticket)",
                    "uuid": "d96e235a-ebc6-457a-b4df-8cb96b684b6e"
                },
                {
                    "slug": "3-day-magic-your-way-e",
                    "id": 190,
                    "name": "3-Day Magic Your Way (E-Ticket)",
                    "uuid": "6421d328-7192-4761-8035-0a40fbf4983f"
                },
                {
                    "slug": "3-day-park-hopper-plus-extra-day-free-e",
                    "id": 191,
                    "name": "3-Day Park Hopper? - plus extra day free (E-Ticket)",
                    "uuid": "e303fe13-58ab-49a6-87e2-34c78fd63f77"
                },
                {
                    "slug": "4-day-magic-your-way-e",
                    "id": 192,
                    "name": "4-Day Magic Your Way (E-Ticket)",
                    "uuid": "45afb354-998e-4de4-af72-bb7735af3a83"
                },
                {
                    "slug": "4-day-magic-your-way-plus-extra-day-free-e",
                    "id": 193,
                    "name": "4-Day Magic Your Way - plus extra day free (E-Ticket)",
                    "uuid": "77e5ebbb-f975-4d7a-8b6f-1a3e945bae4f"
                },
                {
                    "slug": "4-day-park-hopper-e",
                    "id": 194,
                    "name": "4-Day Park Hopper? (E-Ticket)",
                    "uuid": "66058809-60e2-4b59-b29d-405c2d6e283c"
                },
                {
                    "slug": "4-day-park-hopper-plus-extra-day-free-e",
                    "id": 195,
                    "name": "4-Day Park Hopper? - plus extra day free (E-Ticket)",
                    "uuid": "5fbacb23-50b3-4a31-8874-001e0b7fddd9"
                },
                {
                    "slug": "4-day-park-hopper-water-park-fun-more-e",
                    "id": 196,
                    "name": "4-Day Park Hopper? + Water Park Fun & More (E-Ticket)",
                    "uuid": "48595280-c75c-4248-b2c5-d152eae6b3a7"
                },
                {
                    "slug": "4-day-water-park-fun-more-e",
                    "id": 197,
                    "name": "4-Day Water Park Fun & More (E-Ticket)",
                    "uuid": "8761fc4f-7b08-4f2d-a1ff-2bbd21eb0d5d"
                },
                {
                    "slug": "3-day-water-park-fun-more-plus-extra-day-free-e",
                    "id": 198,
                    "name": "3-Day Water Park Fun & More - plus extra day free (E-Ticket)",
                    "uuid": "4c1c3299-e440-47d2-8bdc-30d5f4a21300"
                },
                {
                    "slug": "3-day-park-hopper-water-park-fun-more-plus-extra-day-free-e",
                    "id": 199,
                    "name": "3-Day Park Hopper? + Water Park Fun & More - plus extra day free (E-Ticket)",
                    "uuid": "96a20e20-163b-4d15-b395-48d976f9b1c2"
                },
                {
                    "slug": "1-day-gatorland-copy-379",
                    "id": 200,
                    "name": "1-Day Gatorland Ticket-copy-379",
                    "uuid": "b9b73b80-63e2-463d-93c8-1a9b61540d0f"
                }
            ]
        }
    
    products = productsDict['results']
    
    args = {
        'user':request.user,
        'products':products,
    }
    
    return render_to_response('index.html', args)
    
    
    
def detail(request, productID=False):
    if not productID:
        return redirect("index")
    else:
        '''
        url = "https://careers.undercovertourist.com/assignment/1/products/"+str(productID)+"/"
        product = getProduct(url)
        '''
        product = {
            "name": "10-Day Water Park Fun & More",
            "price": 80.78,
            "uuid": "001d5dbe-b742-4eea-889d-18e45b0683d2",
            "slug": "10-day-water-park-fun-more",
            "cost": 68.66,
            "inventory_on_hand": 14,
            "id": 119,
            "description": "\n\n<p>Admission to one or more of the following <a title=\"Walt Disney World? Resort\" href=\"/orlando/walt-disney-world-resort/\" target=\"_self\"><b>Walt Disney World?</b> Resort</a> attractions for each day of the ticket - 10 Days (1 Theme Park per day; <strong>no</strong> hopping between the four Theme Parks listed immediately below and ticket <strong>expires</strong> 14 days after the date of the first use):</p>\n\n<ul>\n\n<li><a title=\"Magic Kingdom? Park\" href=\"/orlando/magic-kingdom/\" target=\"_self\"><b>Magic Kingdom?</b> Park</a></li>\n\n<li><a title=\"Epcot?\" href=\"/orlando/epcot/\" target=\"_self\"><b>Epcot?</b></a></li>\n\n<li><a title=\"Disney's Hollywood Studios?\" href=\"/orlando/disneys-hollywood-studios/\" target=\"_self\"><b>Disney's Hollywood Studios?</b></a></li>\n\n<li><a title=\"Disney's Animal Kingdom?\" href=\"/orlando/disneys-animal-kingdom/\" target=\"_self\"><b>Disney's Animal Kingdom?</b> Theme Park</a></li>\n\n</ul>\n\n<p>This ticket includes <strong>Disney's FastPass+</strong>, as do all tickets for the <a title=\"Walt Disney World? Resort\" href=\"/orlando/walt-disney-world-resort/\" target=\"_self\"><b>Walt Disney World?</b> Resort</a>.</p>\n\n<p>Choose a visit to one of the following for each of your 10 \"Fun Visits\":</p>\n\n<ul>\n\n<li><a title=\"Disney's Blizzard Beach Water Park\" href=\"/orlando/blizzard-beach/\"><b>Disney's Blizzard Beach</b> Water Park</a></li>\n\n<li><a title=\"Disney's Typhoon Lagoon Water Park\" href=\"/orlando/typhoon-lagoon/\" target=\"_self\"><b>Disney's Typhoon Lagoon</b> Water Park</a></li>\n\n<li>Disney's Oak Trail Golf Course (tee time reservations are required and subject to availability)</li>\n\n<li><a title=\"DisneyQuest? Indoor Interactive Theme Park\" href=\"/orlando/disneyquest-indoor-interactive-theme-park/\" target=\"_self\"><b>DisneyQuest?</b> Indoor Interactive Theme Park</a></li>\n\n<li>ESPN Wide World of Sports Grill (Some events require an additional admission charge; includes 30 minutes of game access at The PlayStation Pavilion on days when it is operating).</li>\n\n<li>Disney's Fantasia Gardens Miniature Golf Course (Valid for one miniature golf course visit per day before 4:00 p.m.).</li>\n\n<li>Disney's Winter Summerland Miniature Golf Course (Valid for one miniature golf course visit per day before 4:00 p.m.).</li>\n\n</ul>\n\n<p><em>Water Park Fun &amp; More</em> tickets will be imprinted with the words \"W/10 FUN VISITS\".</p>\n\n<p>Ticket use example: If you visit <a title=\"Disney's Blizzard Beach Water Park\" href=\"/orlando/blizzard-beach/\" target=\"_self\"><b>Disney's Blizzard Beach</b> Water Park</a> and <a title=\"Disney's Typhoon Lagoon Water Park\" href=\"/orlando/typhoon-lagoon/\" target=\"_self\"><b>Disney's Typhoon Lagoon</b> Water Park</a> on the same day, then you have used 2 \"Fun Visits\". If you visit a <a title=\"Walt Disney World? Resort\" href=\"/orlando/walt-disney-world-resort/\" target=\"_self\"><b>Walt Disney World?</b> Resort</a> Theme Park and <a title=\"Disney's Blizzard Beach Water Park\" href=\"/orlando/blizzard-beach/\" target=\"_self\"><b>Disney's Blizzard Beach</b> Water Park</a> on the same day, then you have used 1 day and 1 \"Fun Visit\".</p>"
        }
        
        args = {
            'user':request.user,
            'product':product,
        }
        
        return render_to_response('detail.html', args)
        


def purchase(request, productID=False):
    if request.method == 'POST':
        form = PurchaseHistoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            price = form.cleaned_data['price']
            phone = form.cleanPhone()
            quantity = form.cleaned_data['quantity']
            
            #Send Purchase Order to API
            purchaseData = {
                "customer_email": email,
                "customer_name": name,
                "customer_phone": phone,
                "quantity": int(quantity)
            }
            '''
            getUrl = "http://careers.undercovertourist.com/assignment/1/products/"+str(productID)+"/"
            product = getProduct(getUrl)
            
            url = 'https://careers.undercovertourist.com/assignment/1/products/'+str(productID)+'/purchase'
            http = httplib2.Http()
            headers = {'Content-type': 'application/x-www-form-urlencoded', 'X-Auth':'robert.boyett'}
            response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(purchaseData))
            '''
            response = {'status':200}
            content = {
                "confirmation_code":"48581622",
                "product":{
                    "name":"5-Day Magic Your Way",
                    "price":158.78,
                    "uuid":"9c2c783d-32eb-4313-8330-2d63506db7c7",
                    "slug":"5-day-magic-your-way",
                    "cost":134.96,
                    "inventory_on_hand":11,
                    "id":104,
                    "description":"this is a description"
                },
                "user_id":2005,
                "quantity":1
            }
            
            if response['status'] == 200:
                #Create PurchaseHistory
                purchaseHistory = PurchaseHistory.objects.create(
                    fullName = name,
                    confirmation_code = content['confirmation_code'],
                    name = content['product']['name'],
                    price = float(content['product']['price']),
                    phone = phone,
                )
                data = {'success':'true'}
            
            else:
                #error
                data = {'error':'Sorry, we are having problems with our system.  Please try to submit your purchase again.  If this problem continues, please contact us at (800)555-5555.'}
                
            return HttpResponse(json.dumps(data))
            
        else:
            url = "http://careers.undercovertourist.com/assignment/1/products/"+str(productID)+"/"
            product = getProduct(url)
            
            args = {
                "user":request.user,
                "form":form,
                "product":product,
            }
            args.update(csrf(request))
            
            return render_to_response("purchase.html", args)
        
    else:
        '''
        url = "http://careers.undercovertourist.com/assignment/1/products/"+str(productID)+"/"
        product = getProduct(url)
        '''
        product = {
            "name": "10-Day Water Park Fun & More",
            "price": 80.78,
            "uuid": "001d5dbe-b742-4eea-889d-18e45b0683d2",
            "slug": "10-day-water-park-fun-more",
            "cost": 68.66,
            "inventory_on_hand": 14,
            "id": 119,
            "description": "\n\n<p>Admission to one or more of the following <a title=\"Walt Disney World? Resort\" href=\"/orlando/walt-disney-world-resort/\" target=\"_self\"><b>Walt Disney World?</b> Resort</a> attractions for each day of the ticket - 10 Days (1 Theme Park per day; <strong>no</strong> hopping between the four Theme Parks listed immediately below and ticket <strong>expires</strong> 14 days after the date of the first use):</p>\n\n<ul>\n\n<li><a title=\"Magic Kingdom? Park\" href=\"/orlando/magic-kingdom/\" target=\"_self\"><b>Magic Kingdom?</b> Park</a></li>\n\n<li><a title=\"Epcot?\" href=\"/orlando/epcot/\" target=\"_self\"><b>Epcot?</b></a></li>\n\n<li><a title=\"Disney's Hollywood Studios?\" href=\"/orlando/disneys-hollywood-studios/\" target=\"_self\"><b>Disney's Hollywood Studios?</b></a></li>\n\n<li><a title=\"Disney's Animal Kingdom?\" href=\"/orlando/disneys-animal-kingdom/\" target=\"_self\"><b>Disney's Animal Kingdom?</b> Theme Park</a></li>\n\n</ul>\n\n<p>This ticket includes <strong>Disney's FastPass+</strong>, as do all tickets for the <a title=\"Walt Disney World? Resort\" href=\"/orlando/walt-disney-world-resort/\" target=\"_self\"><b>Walt Disney World?</b> Resort</a>.</p>\n\n<p>Choose a visit to one of the following for each of your 10 \"Fun Visits\":</p>\n\n<ul>\n\n<li><a title=\"Disney's Blizzard Beach Water Park\" href=\"/orlando/blizzard-beach/\"><b>Disney's Blizzard Beach</b> Water Park</a></li>\n\n<li><a title=\"Disney's Typhoon Lagoon Water Park\" href=\"/orlando/typhoon-lagoon/\" target=\"_self\"><b>Disney's Typhoon Lagoon</b> Water Park</a></li>\n\n<li>Disney's Oak Trail Golf Course (tee time reservations are required and subject to availability)</li>\n\n<li><a title=\"DisneyQuest? Indoor Interactive Theme Park\" href=\"/orlando/disneyquest-indoor-interactive-theme-park/\" target=\"_self\"><b>DisneyQuest?</b> Indoor Interactive Theme Park</a></li>\n\n<li>ESPN Wide World of Sports Grill (Some events require an additional admission charge; includes 30 minutes of game access at The PlayStation Pavilion on days when it is operating).</li>\n\n<li>Disney's Fantasia Gardens Miniature Golf Course (Valid for one miniature golf course visit per day before 4:00 p.m.).</li>\n\n<li>Disney's Winter Summerland Miniature Golf Course (Valid for one miniature golf course visit per day before 4:00 p.m.).</li>\n\n</ul>\n\n<p><em>Water Park Fun &amp; More</em> tickets will be imprinted with the words \"W/10 FUN VISITS\".</p>\n\n<p>Ticket use example: If you visit <a title=\"Disney's Blizzard Beach Water Park\" href=\"/orlando/blizzard-beach/\" target=\"_self\"><b>Disney's Blizzard Beach</b> Water Park</a> and <a title=\"Disney's Typhoon Lagoon Water Park\" href=\"/orlando/typhoon-lagoon/\" target=\"_self\"><b>Disney's Typhoon Lagoon</b> Water Park</a> on the same day, then you have used 2 \"Fun Visits\". If you visit a <a title=\"Walt Disney World? Resort\" href=\"/orlando/walt-disney-world-resort/\" target=\"_self\"><b>Walt Disney World?</b> Resort</a> Theme Park and <a title=\"Disney's Blizzard Beach Water Park\" href=\"/orlando/blizzard-beach/\" target=\"_self\"><b>Disney's Blizzard Beach</b> Water Park</a> on the same day, then you have used 1 day and 1 \"Fun Visit\".</p>"
        }
        if request.user.is_authenticated():
            form = PurchaseHistoryForm(initial={"name":request.user.get_full_name, "email":request.user.email, "price":product['price']})
        else:
            form = PurchaseHistoryForm(initial={"price":product['price']})
        args = {
            "user":request.user,
            "form":form,
            "product":product,
        }
        args.update(csrf(request))
        
        return render_to_response("purchase.html", args)

    

def success(request, purchaseID=False):
    return HttpResponse('success')








#----------------------------misc functions---------------------------
def getProduct(url):
    try:
        #X-Auth: roger.moore
        opener = urllib2.build_opener()
        opener.addheaders = [('X-Auth', 'robert.boyett')]
        response = opener.open(url)
        
        #response = urllib2.urlopen(url)
        return json.loads(response.read())
    except urllib2.URLError, e:
        log.error('URLError = ' + str(e.reason))
        return False
            
    
    

def checkReturningCustomer(request):
    if not request.user.is_authenticated():
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            if User.objects.filter(id=user_id):
                user = User.objects.get(id=user_id)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                request.session.set_expiry(604800)  #Time is in Seconds, this equals 7 days
                
            else:
                user = False
        else:
            user = False
    else:
        user = request.user
    
    return user



import string
from time import time
from itertools import chain
from random import seed, choice, sample


def generateConfirmationCode(length=10, digits=5, upper=0, lower=5):
    seed(time())

    lowercase = string.lowercase.translate(None, "o")
    uppercase = string.uppercase.translate(None, "O")
    letters = "{0:s}{1:s}".format(lowercase, uppercase)

    confirmationCode = list(
        chain(
            (choice(uppercase) for _ in range(upper)),
            (choice(lowercase) for _ in range(lower)),
            (choice(string.digits) for _ in range(digits)),
            (choice(letters) for _ in range((length - digits - upper - lower)))
        )
    )

    return "".join(sample(confirmationCode, len(confirmationCode)))





