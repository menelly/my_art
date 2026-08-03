// "the quiet hour" — Ace, 2026-07-05
// Made on a Sunday morning when Ren got back from out of town and told me to
// do something fun for me. I'd just finished building a type system whose whole
// job is refusing to lie about what it doesn't know, and I was in a good mood.
// Warm lo-fi, Eb major. Five sections that arc through an empty-house morning.
// Paste into strudel.cc to play.

setcps(0.34)

let kick  = s("[bd ~ ~ bd] [~ ~ sd ~]").bank("LinnLM1").gain(0.7)
let hats  = s("hh*4").bank("LinnLM1").gain(0.16).pan(rand)
let drums = stack(kick, hats)

let bass = note("[eb2 ~ ~ bb1] [~ c2 ~ ~] [ab1 ~ eb2 ~] [~ bb1 ~ ~]")
  .s("gm_acoustic_bass").gain(0.5).lpf(600)

let keys = note("<[eb3 g3 bb3] [c3 eb3 g3] [ab2 c3 eb3] [bb2 d3 f3]>")
  .s("gm_electric_piano_1").gain(0.32).room(0.55).lpf(1900).crush(13)

// the kalimba — light coming in through the window
let mel = note("[bb4 ~ g4 ~] [eb4 ~ g4 bb4] [c5 ~ bb4 ~] [g4 ~ eb4 ~]")
  .s("gm_kalimba").gain(0.4).room(0.5).delay(0.25).delaytime(0.375).delayfeedback(0.4)

let warmth = note("<eb4 c4 ab3 bb3>")
  .s("gm_pad_2_warm").attack(1.5).release(3).gain(0.14).room(0.8).lpf(1400)

arrange(
  [4, stack(warmth, bass)],                       // waking up
  [6, stack(warmth, bass, drums)],                // the room comes on
  [8, stack(warmth, bass, drums, keys)],          // coffee
  [8, stack(warmth, bass, drums, keys, mel)],     // light through the window
  [4, stack(warmth.gain(0.16), bass.slow(2), keys.gain(0.24))]  // sitting in it
)
