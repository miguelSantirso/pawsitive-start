# Stage 1 — Welcome Home (Days 1–3). Nothing is demanded of the dog yet.
STAGE = {
    "num": 1,
    "slug": "welcome-home",
    "name": "Welcome Home",
    "emoji": "🏡",
    "color": 1,  # orange
    "when": "Days 1–3",
    "purpose": "Safety, sleep and routine first. Nothing is asked of your dog yet except feeling okay.",
    "intro": "Your new dog is stressed, even if they look happy. Rescue experts describe the first days as a "
             "power-down period: lots of sleeping, nervous sniffing, maybe skipped meals, maybe pacing. "
             "These four exercises create the world your dog needs right now — one safe spot, one boring "
             "routine, one toilet schedule, and food that always comes with good news. Skip the visitors, "
             "the dog park and the big outings; that comes much later.",
    "essentials": [
        "See a vet in the first few days. Bring the shelter records and a fresh stool sample, and ask about parasites, heartworm and vaccination timing for your region.",
        "Register the microchip to your name and address, and add a visible ID tag with your phone number.",
        "Ask your vet about spay or neuter timing rather than assuming a date.",
        "Keep common toxins out of reach: chocolate, grapes and raisins, xylitol (sugar-free gum), onions and garlic.",
    ],
    "exercises": [
        {
            "slug": "safe-space",
            "title": "Build your dog's safe base",
            "emoji": "🛏️",
            "time": "20 minutes to set up, then it lives there",
            "goal": "Your dog has one spot they can always rely on for calm in the room where the family gathers.",
            "why": "In the shelter your dog had almost no control over anything — noise, other dogs, strange "
                   "hands. A safe base gives that control back, and it is one of the most effective stress "
                   "reducers in week one. Many dogs settle faster and bark less when they have a reliable "
                   "spot to retreat to. If a crate came home with you, start gentle familiarization now — "
                   "meals near it, door open — "
                   "and the full alone-time ladder waits for Stage 5.",
            "need": ["A bed or crate (door open)", "One towel or blanket", "Water bowl", "A few soft treats"],
            "steps": [
                "Pick one room where the family normally sits, and a calm corner of it away from doorways.",
                "Set up the bed or crate with two escape routes visible — never pin them in with furniture.",
                "Make it dim and cosy: bedding, a towel with their (or the shelter's) smell, low light.",
                "Place the water bowl beside it, not inside it.",
                "Say the rule out loud to the whole household, kids included: when the dog is on their bed, nothing happens to them. No petting, no calling, no pulling.",
                "Each day, sit on the floor a few feet away doing your own quiet thing, and occasionally toss a treat near the bed. Then walk away. Let them discover it.",
            ],
            "criteria": [
                "Your dog walks onto the bed or into the crate all by themselves, at least twice.",
                "They sleep or chew there while normal household life carries on around them.",
            ],
            "mistakes": [
                "Never drag or push them onto it — the spot only works because it's the one place nothing is done to them.",
                "Don't put it next to a rumbling appliance or beside a door that bangs.",
                "Don't turn the crate into a punishment zone — banishment ruins it.",
            ],
            "trouble": [
                {"q": "My dog hides under the actual bed instead.",
                 "a": "Hiding spots are safe spaces too. Use that corner for now and quietly make it comfortable; you can move the proper bed beside it next week."},
                {"q": "They just pace and won't lie down anywhere.",
                 "a": "Sit by the bed with a chew, yawn slowly, keep your shoulders low. Many dogs begin to settle in the first days, but decompression can take weeks or months; let your dog set the pace. Most adult dogs sleep 12–14 hours, and stressed dogs may sleep more. If your dog is hard to rouse or not eating, call the vet."},
            ],
            "source": {"label": "VCA: how to crate train your dog", "url": "https://vcahospitals.com/know-your-pet/how-to-crate-train-your-dog"},
        },
        {
            "slug": "do-nothing-sitting",
            "title": "The daily nothing habit",
            "emoji": "🧘",
            "time": "10–20 minutes, twice a day",
            "goal": "Sit near your dog with zero demands, letting them study you and relax without performing.",
            "why": "First-time owners usually rush interaction — touching, calling, playing. A guarded rescue "
                   "dog needs the opposite: passive company. Slowly, your presence becomes background noise "
                   "they can relax next to, which is how attachment actually starts.",
            "need": ["A chair or floor spot", "Something quiet to read"],
            "steps": [
                "Pick two calm moments a day — morning coffee, evening wind-down.",
                "Sit or lie low near where your dog settles, angled slightly sideways, not squared-up facing them.",
                "Stay off your phone and say nothing for 10–20 minutes.",
                "If they stare at you, give a soft look-away. Soft, brief glances only — no staring contests.",
                "If they come close to sniff you, let them take the time. Touch nothing unless they clearly lean against you.",
                "End on time — or sooner if your dog is stressed.",
            ],
            "criteria": [
                "Your dog stays settled within a few feet of you for most of the session.",
                "You spot real relaxation signals: a heavy yawn, slow blinks, a shake-off, slow chews.",
            ],
            "mistakes": [
                "Don't fill the silence with commands or chatter — nothing is being asked.",
                "Don't loom or initiate surprise hugs; contact is always their idea.",
                "Don't use this slot to brush, wipe paws or trim → it must stay boring.",
            ],
            "trouble": [
                {"q": "They hover and whine at me the whole time.",
                 "a": "Whining is often the dog asking 'what do you want?' — being predictably boring answers it. Shorten the sit to 5 minutes twice a day for a few days."},
                {"q": "They fall asleep instantly — every time.",
                 "a": "That is the exercise working. Falling asleep near you is a big trust milestone; keep it going."},
            ],
        },
        {
            "slug": "toilet-routine",
            "title": "The toilet drill that prevents accidents",
            "emoji": "🚽",
            "time": "5 minutes per trip, on schedule all day",
            "goal": "One toilet spot, one schedule, big rewards — before accidents can happen, not after.",
            "why": "Assume your dog is not house-trained, even if the shelter says otherwise: routines break in "
                   "shelters, and stress alone causes accidents. Going back to an hourly-plus-triggers schedule "
                   "whether they 'seem fine' or not is how every good rescue house-training guide handles it — "
                   "and preventing mistakes beats reacting to them every single time.",
            "need": ["One chosen toilet spot", "Treats stationed by the door", "Meal-time schedule", "Lead and harness"],
            "steps": [
                "Pick the spot and the door — always the same patch, always the same route out.",
                "Write the schedule: immediately on waking, 10 minutes after every meal or big drink, after every nap and play session, roughly hourly in between while awake, and last thing at night. Put phone alerts on.",
                "Clip the lead on, walk calmly to the spot, and say your phrase once ('go potty').",
                "Stand still and boring for 3–4 minutes. Sniffing first is normal and part of the process.",
                "The second they finish — praise and deliver a treat while still outside on the spot.",
                "Come back inside; keep the dog with you or pen them so a quiet corner accident isn't possible, then try again in 10–15 minutes.",
                "Any accident: say nothing, blot it, clean with an enzyme cleaner, go 10 minutes earlier next time, and jot down when it happened to spot their pattern.",
            ],
            "criteria": [
                "Accidents are rare and decreasing over five days while you keep the schedule.",
                "Your dog heads for the door or the spot when they need to go, most times.",
            ],
            "mistakes": [
                "Never punish accidents. Scolded dogs don't learn bladder control — they learn to fear toilet visits and hide in the laundry.",
                "Don't change spots, wording or door each time; sameness is what teaches.",
                "Don't rush back indoors instantly after they finish — stay a moment so 'going outside' isn't immediately 'the fun ends'.",
            ],
            "trouble": [
                {"q": "They come right back inside and go.",
                 "a": "They were too tense to go outside yet — classic in new rescues. Wait longer outside quietly, or toss a treat into the patch of grass to help them relax. Go back in only after a success or your full 3–4 minutes."},
                {"q": "Night-time accidents only.",
                 "a": "Don't withhold water unless your vet specifically advises it. If your vet agrees, take up the bowl after the last trip; always leave water available in hot weather or for dogs on medication. Last trip right before sleep, and pen them next to the bed the first week."},
                {"q": "They seem to go anywhere at all, constantly.",
                 "a": "Tether them to your belt indoors ('umbilical training') for a few days, and mention it at the vet — infections and parasites are common causes of accidents in shelter dogs."},
            ],
            "source": {"label": "Housetraining survival guide (Animal Humane Society)", "url": "https://www.animalhumanesociety.org/resource/housetraining-survival-guide"},
        },
        {
            "slug": "scatter-hand-feed",
            "title": "Every meal becomes a good-news game",
            "emoji": "🍖",
            "time": "5–10 minutes per meal",
            "goal": "Split every meal into sniffing, hand-feeding and puzzle parts, so you become the best thing in their day.",
            "why": "Food is the fastest trust-builder you have. Hand-feeding and scatter-feeding teach your dog that "
                   "good things happen near this human — not just that people take things away. Sniffing out food "
                   "also settles an anxious body, and your dog learns that learning from you pays.",
            "need": ["Their daily food ration", "A mat or grass patch", "A stuffed Kong or puzzle toy", "A quiet corner"],
            "steps": [
                "Split today's food into 3–4 portions.",
                "Portion 1: scatter it on a mat, or in your own yard once your vet confirms vaccination status; avoid public grass until then. Let them 'find it' — this is the sniff game.",
                "Portion 2: hand-feed a few pieces at a time from your flat palm, asking for nothing, saying nothing.",
                "Portion 3: stuff a puzzle toy or frozen Kong for after, in their safe spot.",
                "Reserve a small handful as jackpots (extra-big payouts) for moments later in the day (new things, brave moments).",
                "Pick up unfinished food only after the meal window; never snatch a bowl or chew the dog is still using — trade if you need it back. No free-feeding from an always-full bowl.",
            ],
            "criteria": [
                "Your dog perks up at the sound of your approach at meal times.",
                "They take food from your open palm in one calm meeting per day.",
            ],
            "mistakes": [
                "Never hover, reach or lean over their food — you're the source of good things, not a guard.",
                "Don't skip meals to 'build appetite' — to a stressed dog, a skipped meal reads as scarcity. If your dog still isn't eating after a day, ask the vet before changing anything.",
                "Don't let kids crawl near feeding time — ever, in every week and every stage of this course.",
            ],
            "trouble": [
                {"q": "They won't eat at all.",
                 "a": "Normal for the first days — stress kills appetite. Toss food from a distance and back off; if they truly eat nothing for 24+ hours, call the vet."},
                {"q": "They wolf food and seem edgy when I pass by.",
                 "a": "Scatter from further away NOW; stand beyond arm's reach, and let approach shrink over weeks — see the bowl exercise in Stage 5 before ever going closer."},
            ],
        },
    ],
}
