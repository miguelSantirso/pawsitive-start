# Stage 6 — Growing Together (Months 3–6): reliability, joy, and the graduation plan.
STAGE = {
    "num": 6,
    "slug": "growing-together",
    "name": "Growing Together",
    "emoji": "🏆",
    "color": 6,  # green
    "when": "Months 3–6",
    "purpose": "Prove recall outdoors, add joy with tricks, polish guest and car manners, and set your next goals.",
    "intro": "By now your dog knows the language, walks with a slack leash, rests alone and gives you consent. "
             "This stage is where trust becomes joy: an outdoor recall you can actually count on, two tricks "
             "that make guests smile, calm guest arrivals and car rides, and a graduation plan that keeps you "
             "training into year one. It's also the stage where you decide together what 'a good life for "
             "this particular dog' looks like.",
    "exercises": [
        {
            "slug": "long-line-recall",
            "tags": ["leash", "bonding"],
            "seq": True,
            "seq_after": "indoor-recall",
            "seq_reason": "the indoor come game comes first, then the same promise moves outdoors on a long line.",
            "title": "Outdoor come-on-a-line",
            "emoji": "🎉",
            "time": "5 minutes × 3 a week",
            "goal": "From 20+ feet outdoors, on one call, your dog turns and comes straight back to you.",
            "why": "Outdoor recall is the rescue life-saver — and freedom is earned on a long line first, never by "
                   "gambling. One bad recall is a setback, not a reset; keep the pay generous and the promise "
                   "strong: come = a big reward.",
            "need": ["A 15–30 ft long line clipped to a well-fitted harness", "Their all-time favorite treat (cheese, chicken...)", "A quiet field or yard", "A long-lasting toy for some recalls"],
            "steps": [
                "Clip the long line to a well-fitted harness (never a flat collar) in a quiet area and let them wander a few feet.",
                "Say 'Name! Come!' once, crouch, and run backwards two or three steps — the running-away dog is far more interesting than the calling dog.",
                "On arrival: 'Yes!' then the full jackpot (ten tiny treats tossed to graze) or a toy game. Vary it — sometimes food, sometimes play, sometimes release right back to sniffing ('go sniff!' as a reward too).",
                "Call when they're mid-sniff a few feet away: pay huge. If they don't come, quietly take up the line and reset at a shorter distance — no second call.",
                "Grow distance as the success rate holds: 10 ft → 20 ft → 30 ft, indoors→garden→field.",
                "Never call to end something great — call, pay, then release them back to it. Recall shouldn't end life's best moments.",
                "Proof it: a friend stands at 30 feet eating a sandwich, other dogs visible 50 feet off — call once, pay generous arrivals. Freedom always begins below these thresholds.",
            ],
            "criteria": [
                "9 out of 10 recalls at 20 feet with mild distractions, arriving fast and happy.",
                "They turn at the FIRST call — no repeats, no slow 'should I bother?' hesitation.",
            ],
            "mistakes": [
                "Repeat-calling teaches the dog to wait for the third call; one call, then act (walk the line, reset easier).",
                "Never punish a returning dog or grab their collar harshly on arrival — the collar becomes recall's nemesis otherwise.",
                "No off-leash freedom in unfenced areas until this is proven across many places — the long line is the plan, for months if needed.",
            ],
            "trouble": [
                {"q": "Great indoors, absent outdoors.",
                 "a": "Outdoor money is different currency: pay hamburger, not kibble, outdoors. Early on, pay EVERY outdoor response for a solid two weeks."},
                {"q": "They come but keep a foot beyond arm's reach.",
                 "a": "Feed tosses AT your feet, pay from the ground, and practice 'come = feet near feet' with the collar-touch game; distance-dodging is usually a handler-speed problem, not defiance."},
            ],
        },
        {
            "slug": "spin-trick",
            "tags": ["bonding"],
            "core": False,
            "title": "Trick: spin",
            "emoji": "🌀",
            "time": "2 minutes × 2 a day",
            "goal": "One full circle on cue — the confidence trick that teaches 'learning with you is the fun part'.",
            "why": "After weeks of careful rescue-building, tricks are where dogs find out that training is play. "
                   "Spinning builds body awareness and gives the dog a fun job, and gives nervous dogs a friendly, "
                   "rehearsed job to do in awkward moments (guest arrival, vet waiting room).",
            "need": ["Treats", "A clear floor spot", "Two minutes of positive mood (yours and theirs)"],
            "steps": [
                "Hold a treat at nose height and lure a small, tight circle around their own body.",
                "Mark the halfway point ('Yes!', treat), then on a later rep mark the full circle and treat — jackpot it.",
                "When the circle is smooth, try the same motion with an empty hand — mark and pay from the other hand.",
                "Add the cue 'spin' as the gesture matures; keep the hand sweep, smaller and smaller.",
                "Keep it one direction for a while; the other direction is a different trick and gets its own cue later.",
                "Two or three reps per session max. Tricks end while they're still having fun.",
            ],
            "criteria": [
                "One clean full spin on the verbal cue with the gesture nearly invisible.",
                "Performs it for a friend or in a new room — the trick survives new situations.",
            ],
            "mistakes": [
                "Don't drill until dizzy or bored — two good reps beat ten tired ones.",
                "Don't hand-cue forever; the voice should carry it eventually.",
                "Don't use tricks as 'make them move when scared' — spin is play, not a steering wheel.",
            ],
            "trouble": [
                {"q": "They won't follow the lure at all.",
                 "a": "Walk the circle yourself — your movement drags their focus better than a still lure for anxious dogs; shrink the circle as they tune in."},
                {"q": "They spin and keep spinning.",
                 "a": "It's become a self-reward game — pay after ONE circle, then ask something different ('sit') to break the loop."},
            ],
        },
        {
            "slug": "high-five",
            "tags": ["bonding"],
            "core": False,
            "title": "Trick: high five",
            "emoji": "🖐️",
            "time": "2 minutes × 2 a day",
            "goal": "Their paw lands on your open palm on cue — the polite 'job' for greetings.",
            "why": "High five pairs paw-touch with good things, and gives excitable dogs "
                   "a rehearsed 'polite job' when guests arrive instead of jumping. Two-syllable plus paw = the "
                   "trick every guest remembers.",
            "need": ["Treats in a closed fist", "A sit cue they know"],
            "steps": [
                "Ask for a sit.",
                "Hold a treat in your closed fist at paw height, just in front of a shoulder.",
                "They'll paw or bat at the fist: mark 'Yes!' the instant the paw rises and taps — then open the hand and pay.",
                "Repeat: same game, empty fist, mark the paw tap, open hand to show, pay from the other hand.",
                "Add the cue 'high five' once the tap is reliable.",
                "Switch to the open palm low, then gradually raise palm height over sessions.",
                "Vary the hands and the person — the dog generalizes when the trick survives a friend's palm.",
            ],
            "criteria": [
                "Paw lands on your open palm on cue, 9 of 10 tries.",
                "They offer it in a new place or to another person.",
            ],
            "mistakes": [
                "Never grab and lift their paw to 'show' them — paw handling stays consent-based, like all Stage 5 handling.",
                "Don't drill it to sore shoulders — two reps at a time.",
                "Don't expect it with strangers before it's boredom-proof with you.",
            ],
            "trouble": [
                {"q": "They stare at the fist but never paw.",
                 "a": "Wiggle the fingers a little (tickle effect), or brush your hand lightly against their leg so lifting the paw beats frustration; mark the smallest lift at first."},
                {"q": "They try the mouth instead of the paw.",
                 "a": "Hold the fist a touch higher and closer to the shoulder; nose can't reach it, but paw can."},
            ],
        },
        {
            "slug": "guest-doors",
            "tags": ["home-life", "calm"],
            "title": "Guest arrivals without chaos",
            "emoji": "🚪",
            "time": "Rehearse 5–10 minutes weekly",
            "goal": "Knock → they go to the mat → they stay until released → they greet with four feet on the floor.",
            "why": "Excited greeting moments are where escapes, bites and 'good luck with the new "
                   "dog' stories get made. A rehearsed arrival ritual protects everyone — and it's the "
                   "home version of the Canine Good Citizen 'friendly stranger' item.",
            "need": ["A helper", "Their mat from Stage 3", "Treats", "A gate for real deliveries meanwhile"],
            "steps": [
                "Rehearse the sequence without a guest first: you knock loudly yourself, dog to mat, mark and treat.",
                "Next: helper knocks; helper STAYS outside until the dog is settled on the mat.",
                "Door opens; dog stays on the mat; helper walks in and ignores the dog COMPLETELY for about 10 seconds.",
                "Release word ('go say hi'); the helper stands sideways and lets the dog approach — no leaning over, no face-to-face, no overhead hands.",
                "If they jump: helper turns silently away, and send them back to the mat. No shouting, no grabbing.",
                "Repeat with different helpers over a few weeks — same ritual, calmer dog, every time.",
                "Real deliveries meanwhile get the gate: management while the ritual solidifies.",
            ],
            "criteria": [
                "They trot to their mat at the sound of the knock.",
                "They stay until released, and greet without jumping — even with a new person arriving.",
            ],
            "mistakes": [
                "Never collar-grab at the door — grabbing an excited dog can turn excitement into fear or a bite; use the ritual + the gate.",
                "Don't let guests reward jumping with attention ('no, but I LOVE dogs!') — every guest follows the ignore-until-released rule.",
                "Don't skip the rehearsal — real guests are exam day, not the class.",
            ],
            "trouble": [
                {"q": "They ignore the mat completely when the doorbell rings.",
                 "a": "Dial it back: ring a quiet recording of the bell, feed at the mat, repeat a dozen calm times from the hallway to the door. Real bell = too thrilling to learn at first."},
                {"q": "Guests keep sneaking pets anyway.",
                 "a": "Post a small sign by the door while training — 'Dog in training: I'll greet you when I'm ready'. Most guests will respect the sign; if they don't, keep the dog behind the gate."},
            ],
        },
        {
            "slug": "car-calm",
            "tags": ["calm", "home-life"],
            "title": "Car rides without panic",
            "emoji": "🚗",
            "time": "10 minutes × 2 a week",
            "goal": "Load on cue, settle or nap during the drive, and unload politely — no drool, no scramble.",
            "why": "Many rescues have car histories you'll never know: transport cages, one-way trips, a history of fear. "
                   "Cars matter for vet visits and emergencies, so we rebuild them slow: parked car = snack place, "
                   "engine on = nothing happens, one-minute drives = micro-adventures.",
            "need": ["Treats", "A crash-tested harness or secured crate", "A stuffed chew", "Short destination list (park! NOT the vet first)"],
            "steps": [
                "Explore the parked, engine-off car with the door open: treats around, inside, on the floor.",
                "Feed a meal or a chew in the car — and from now on the food toy in the car is car-ONLY (a separate one from the departure toy), so car = special snack place.",
                "Say the new cue 'up' as you lure the hop onto the back seat, then mark, treat, and hop straight back out.",
                "Sit in the car together, engine off, for five minutes of treat scattering — no destination, no pressure.",
                "Engine on, no movement, two minutes, treats. Nothing happening is the lesson.",
                "Gradually: engine on → roll down the drive → one street, then park; build to ten and twenty minutes over weeks.",
                "Always arrive somewhere NICE early in this training (the park). If a vet trip is needed before car training is finished, use a secured crate and ask the clinic for a quiet entrance — don't delay care.",
            ],
            "criteria": [
                "They load onto the seat within ten seconds of the 'up' cue.",
                "They settle or nap within five minutes of driving — no frantic pacing or drooling on a 15-minute ride.",
            ],
            "mistakes": [
                "Don't drive with them loose in the cabin or poking out the front window — restraint is safety AND calm.",
                "Don't make the first destination the clinic; anxious associations from day one linger for months.",
                "Don't scold drool or crying — pace, treat placement and shorter trips are the medicine.",
            ],
            "trouble": [
                {"q": "They refuse to load.",
                 "a": "Back several rungs and park the car for three days with treats inside only when nobody pushes; some dogs need weeks of 'car = neutral' before 'car = good'. Severe, shaking refusal = a force-free behaviorist; motion sickness is also treatable — ask the vet."},
                {"q": "Jumping straight back out.",
                 "a": "Feed the stuffed toy ON the seat while YOU sit in the back; build 'stay in the seat' with treats BEFORE the engine ever turns."},
            ],
        },
        {
            "slug": "graduation-plan",
            "tags": ["home-life", "bonding"],
            "title": "Graduation: the next 30 days",
            "emoji": "🎓",
            "time": "One planning hour, once",
            "goal": "Turn course progress into a written plan — your two weakest skills, a class or evaluator, and your year-one goals.",
            "why": "Courses don't finish behavior change; they hand off a plan. The Canine Good Citizen checklist is "
                   "a proven everyday-manners map of 10 items, and picking your own two weakest gives you exactly "
                   "the right homework instead of a vague 'keep training'. A written plan can help owners keep training going.",
            "need": ["The CGC test-items link below", "A pen", "A reward-based class nearby if you want one"],
            "steps": [
                "Score your dog against the 10-item manners checklist (Canine Good Citizen items — see the 'Learn more' link below): mark each one done / needs work.",
                "Circle the TWO weakest items — those are your training focus for the next month, a few 2–5 minute sessions most days.",
                "Use the three D's test each skill monthly: can they hold it longer, from farther, with more going on?",
                "Book a reward-based class or ask a reward-based trainer for an eval — check they're force-free before you sign up (ask what happens when the dog gets it wrong).",
                "Keep the joy alive: weekly sniffari, food puzzles, one new trick a month, and a photo dump you like.",
                "Know your escalation triggers and write them down: aggression or bites, panic when alone, guarding that grows — that's the point you call a certified pro (CAAB/DACVB or CPDT-KA).",
                "Celebrate: these foundation skills make everyday life easier and give you a clear plan; keep practicing to protect the bond.",
            ],
            "criteria": [
                "Your next-30-days plan is written down with two focus skills and dates.",
                "A class or trainer is booked (or the decision made that home training continues alone).",
            ],
            "mistakes": [
                "Don't stop training because it 'works now' — the first month-off is where proofing is lost.",
                "Don't compare your dog's pace to anyone's — shelter dogs arrive with invisible histories and unmeasurable setbacks.",
                "Don't skip the annual vet re-check or fall behind on vaccine/prevention plans — health underlies behavior.",
            ],
            "trouble": [
                {"q": "I can't pick which two skills are weakest.",
                 "a": "Ask two people who see your dog regularly, or film a week of normal life and watch it with the checklist next to you — the honest gaps usually show up on video in minutes."},
                {"q": "No reward-based trainer in my area.",
                 "a": "Ask for online consultations (most force-free pros offer video coaching now), and lean on the source links in this course — every exercise here is designed to be self-guided."},
            ],
            "source": {"label": "Canine Good Citizen test items", "url": "https://www.akc.org/products-services/training-programs/canine-good-citizen/canine-good-citizen-test-items/"},
        },
    ],
}
