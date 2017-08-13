vehicle_list = (
    ("Landstalker", 400), # CAR
    ("Bravura", 401), # CAR
    ("Buffalo", 402), # CAR_FAST
    ("Linerunner", 403), # HEAVY
    ("Perennial", 404), # CAR
    ("Sentinel", 405), # CAR
    ("Dumper", 406), # HEAVY
    ("Fire Truck", 407), # HEAVY
    ("Trashmaster", 408), # HEAVY
    ("Stretch", 409), # HEAVY
    ("Manana", 410), # CAR
    ("Infernus", 411), # CAR_FAST
    ("Voodoo", 412), # CAR
    ("Pony", 413), # CAR
    ("Mule", 414), # CAR
    ("Cheetah", 415), # CAR_FAST
    ("Ambulance", 416), # HEAVY
    ("Leviathan", 417), # HELI
    ("Moonbeam", 418), # CAR
    ("Esperanto", 419), # CAR
    ("Taxi", 420), # CAR
    ("Washington", 421), # CAR
    ("Bobcat", 422), # CAR
    ("Mr. Whoopee", 423), # HEAVY
    ("BF Injection", 424), # CAR
    ("Hunter", 425), # HELI
    ("Premier", 426), # CAR
    ("Enforcer", 427), # HEAVY
    ("Securicar", 428), # HEAVY
    ("Banshee", 429), # CAR_FAST
    ("Predator", 430), # BOAT
    ("Bus", 431), # HEAVY
    ("Rhino", 432), # HEAVY

    # tank...
    ("Barracks", 433), # HEAVY
    ("Hotknife", 434), # CAR_FAST
    ("Artict Trailer", 435), # TRAILER
    ("Previon", 436), # CAR
    ("Coach", 437), # HEAVY
    ("Cabbie", 438), # CAR
    ("Stallion", 439), # CAR_FAST
    ("Rumpo", 440), # CAR
    ("RC Bandit", 441), # MINI
    ("Romero", 442), # CAR
    ("Packer", 443), # HEAVY
    ("Monster", 444), # HEAVY
    ("Admiral", 445), # CAR
    ("Squalo", 446), # BOAT
    ("Seasparrow", 447), # HELI
    ("Pizza Boy", 448), # BIKE

    # needs to be researched to find actual max passengers in SA:MP
    ("Trolly", 449), # HEAVY

    # train...
    ("Artict Trailer 2", 450), # TRAILER
    ("Turismo", 451), # CAR_FAST
    ("Speeder", 452), # BOAT
    ("Reefer", 453), # BOAT
    ("Tropic", 454), # BOAT
    ("Flatbed", 455), # HEAVY
    ("Yankee", 456), # HEAVY
    ("Caddy", 457), # MINI
    ("Solair", 458), # CAR
    ("Berkley's RC Van", 459), # HEAVY
    ("Skimmer", 460), # AIRPLANE
    ("PCJ-600", 461), # BIKE
    ("Faggio", 462), # BIKE
    ("Freeway", 463), # BIKE
    ("RC Baron", 464), # MINI
    ("RC Raider", 465), # MINI
    ("Glendale", 466), # CAR
    ("Oceanic", 467), # CAR
    ("Sanchez", 468), # BIKE
    ("Sparrow", 469), # HELI
    ("Patriot", 470), # CAR
    ("Quadbike", 471), # BIKE

    # sort of..
    ("Coastguard", 472), # BOAT
    ("Dinghy", 473), # BOAT
    ("Hermes", 474), # CAR
    ("Sabre", 475), # CAR
    ("Rustler", 476), # AIRPLANE
    ("ZR-350", 477), # CAR_FAST
    ("Walton", 478), # CAR
    ("Regina", 479), # CAR
    ("Comet", 480), # CAR_FAST
    ("BMX", 481), # BIKE
    ("Burrito", 482), # HEAVY

    # more research on this, the side door might allow 2 passengers
    ("Camper", 483), # HEAVY
    ("Marquis", 484), # BOAT
    ("Baggage", 485), # MINI
    ("Dozer", 486), # HEAVY
    ("Maverick", 487), # HELI
    ("News Chopper", 488), # HELI
    ("Rancher", 489), # CAR
    ("FBI Rancher", 490), # CAR
    ("Virgo", 491), # CAR
    ("Greenwood", 492), # CAR
    ("Jetmax", 493), # BOAT
    ("Hotring Racer", 494), # CAR_FAST
    ("Sandking", 495), # CAR
    ("Blista Compact", 496), # CAR
    ("Police Maverick", 497), # HELI
    ("Boxville", 498), # HEAVY
    ("Benson", 499), # HEAVY
    ("Mesa", 500), # CAR
    ("RC Goblin", 501), # MINI
    ("Hotring Racer 2", 502), # CAR_FAST
    ("Hotring Racer 3", 503), # CAR_FAST
    ("Bloodring Banger", 504), # CAR_FAST
    ("Rancher", 505), # CAR
    ("Super GT", 506), # CAR_FAST
    ("Elegant", 507), # CAR
    ("Journey", 508), # HEAVY
    ("Bike", 509), # BIKE
    ("Mountain Bike", 510), # BIKE
    ("Beagle", 511), # AIRPLANE
    ("Cropduster", 512), # AIRPLANE
    ("Stuntplane", 513), # AIRPLANE
    ("Tanker", 514), # HEAVY

    # semi truck
    ("Roadtrain", 515), # HEAVY

    # semi truck
    ("Nebula", 516), # CAR
    ("Majestic", 517), # CAR
    ("Buccaneer", 518), # CAR
    ("Shamal", 519), # AIRPLANE
    ("Hydra", 520), # AIRPLANE
    ("FCR-900", 521), # BIKE
    ("NRG-500", 522), # BIKE
    ("HPV1000", 523), # BIKE
    ("Cement Truck", 524), # HEAVY
    ("Towtruck", 525), # HEAVY
    ("Fortune", 526), # CAR
    ("Cadrona", 527), # CAR
    ("FBI Truck", 528), # HEAVY
    ("Willard", 529), # CAR
    ("Forklift", 530), # MINI
    ("Tractor", 531), # CAR
    ("Combine Harvester", 532), # HEAVY
    ("Feltzer", 533), # CAR
    ("Remington", 534), # CAR
    ("Slamvan", 535), # CAR_FAST
    ("Blade", 536), # CAR_FAST
    ("Freight", 537), # HEAVY

    # train engine...
    ("Brown Streak Engine", 538), # HEAVY

    # train engine...
    ("Vortex", 539), # BOAT
    ("Vincent", 540), # CAR
    ("Bullet", 541), # CAR_FAST
    ("Clover", 542), # CAR
    ("Sadler", 543), # CAR
    ("Fire Truck with ladder", 544), # HEAVY
    ("Hustler", 545), # CAR
    ("Intruder", 546), # CAR
    ("Primo", 547), # CAR
    ("Cargobob", 548), # HELI
    ("Tampa", 549), # CAR
    ("Sunrise", 550), # CAR
    ("Merit", 551), # CAR
    ("Utility Van", 552), # HEAVY
    ("Nevada", 553), # AIRPLANE
    ("Yosemite", 554), # CAR
    ("Windsor", 555), # CAR
    ("Monster 2", 556), # HEAVY
    ("Monster 3", 557), # HEAVY
    ("Uranus", 558), # CAR_FAST
    ("Jester", 559), # CAR_FAST
    ("Sultan", 560), # CAR_FAST
    ("Stratum", 561), # CAR
    ("Elegy", 562), # CAR_FAST
    ("Raindance", 563), # HELI
    ("RC Tiger", 564), # MINI
    ("Flash", 565), # CAR
    ("Tahoma", 566), # CAR
    ("Savanna", 567), # CAR
    ("Bandito", 568), # CAR_FAST
    ("Freight Train Flatbed", 569), # HEAVY

    # train car...
    ("Brown Streak", 570), # HEAVY

    # train car... XXX dupe, streakc
    ("Kart", 571), # MINI
    ("Mower", 572), # MINI
    ("Dune", 573), # HEAVY
    ("Sweeper", 574), # MINI
    ("Broadway", 575), # CAR
    ("Tornado", 576), # CAR
    ("AT-400", 577), # AIRPLANE
    ("DFT-30", 578), # HEAVY

    # large flat-bed truck
    ("Huntley", 579), # CAR
    ("Stafford", 580), # CAR
    ("BF-400", 581), # BIKE
    ("News Van", 582), # HEAVY
    ("Tug", 583), # MINI
    ("Petrol Trailer", 584), # TRAILER
    ("Emperor", 585), # CAR
    ("Wayfarer", 586), # BIKE
    ("Euros", 587), # CAR_FAST
    ("Hotdog", 588), # HEAVY
    ("Club", 589), # CAR
    ("Freight Train Boxcar", 590), # HEAVY

    # train car...
    ("Artict Trailer 3", 591), # TRAILER
    ("Andromada", 592), # AIRPLANE
    ("Dodo", 593), # AIRPLANE
    ("RC Cam", 594), # MINI
    ("Launch", 595), # BOAT
    ("Police Car (LS)", 596), # CAR
    ("Police Car (SF)", 597), # CAR
    ("Police Car (LV)", 598), # CAR
    ("Police Ranger", 599), # CAR
    ("Picador", 600), # CAR
    ("S.W.A.T.", 601), # HEAVY
    ("Alpha", 602), # CAR_FAST
    ("Phoenix", 603), # CAR_FAST
    ("Damaged Glendale", 604), # CAR
    ("Damaged Sadler", 605), # CAR
    ("Baggage Trailer", 606), # TRAILER
    ("Baggage Trailer 2", 607), # TRAILER
    ("Tug Staircase", 608), # TRAILER
    ("Black Boxville", 609), # HEAVY
    ("Farm Trailer", 610), # TRAILER
    ("Street Sweeper Trailer", 611) # TRAILER
)