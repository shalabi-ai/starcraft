'''
Commander Unit

A combat unit that is unique to a commander and is directly created, recruited, summoned, evolved, or controlled by
that commander as a persistent member of their army.

Characteristics:

1- Unique to a commander.
2- Controllable by the player.
3- Persistent and expected to remain part of the army until destroyed.
4- Represents a standing army asset rather than a temporary ability effect.

Rule of thumb:

If a player loses the unit and would naturally say, "I lost one of my units," it is probably a Commander Unit. If the
entity primarily exists because an ability was activated and disappears after performing its function, it is probably
a Commander Ability Asset.
'''
COMMANDER_UNITS = {
    # Alarak
    "Supplicant",
    "HighTemplarTaldarim",
    "WarpPrismTaldarim",
    "WarpPrismPhasingTaldarim",
    "ColossusTaldarim",
    "ImmortalTaldarim"
    "VoidRayTaldarim",

    # Abathur
    "AbathurSymbioteBrutalisk",
    "Brutalisk",
    "HotSLeviathan",
    "RavagerAbathur",
    "RoachVile",


    # Nova
    "Marine_BlackOps",
    "Marauder_BlackOps",
    "Ghost_BlackOps",
    "GhostFemale_BlackOps",
    "HellbatBlackOps",
    "Goliath_BlackOps",
    "SiegeTank_BlackOps",
    "SiegeTankSieged_BlackOps",
    "Raven_BlackOps",
    "Banshee_BlackOps",
    "Liberator_BlackOps",
    "LiberatorAG_BlackOps",


    # Tychus
    "TychusFirebat",
    "TychusGhost",
    "TychusMarauder",
    "TychusMedic",
    "TychusReaper",
    "TychusSpectre",
    "TychusWarhound",
    "TychusHERC",

    # Stukov
    "SIInfestedMarine",
    "SIInfestedTrooper",
    "StukovInfestedDiamondBack",
    "StukovInfestedSiegeTank",
    "StukovInfestedBanshee",
    "SILiberator",

    # Dehaka
    "DehakaRoachLevel2",
    "DehakaHydraliskLevel2",
    "DehakaMutaliskLevel3",
    "DehakaGuardian",
    "DehakaPrimalSwarmHost",
    "DehakaUltraliskLevel3",

    # Karax
    "ZealotPurifier",
    "SentryPurifier",
    "ImmortalAiur",
    "ColossusPurifier",
    "PhoenixPurifier",
    "CarrierAiur",

    # Fenix
    "AdeptFenix",
    "SentryFenix",
    "FenixKaldalisZealot",
    "FenixTalisAdept",
    "FenixTaldarinImmortal",
    "FenixWarbringerColossus",
    "FenixMojoScout",
    "FenixClolarionCarrier",


    # Stetmann
    "ZerglingStetmann",
    "HydraliskStetmann",
    "UltraliskStetmann",
    "CorruptorStetmann",

    # Zeratul
    "ZeratulDarkTemplar",
    "ZeratulStalker",
    "ZeratulSentry",
    "ZeratulImmortal",
    "ZeratulDisruptor",

    # Vorazun
    "ZealotShakuras",
    "StalkerShakuras",
    "DarkTemplarShakuras",
    "CorsairMP",
    "VoidRayShakuras",

    # Swann
    "Hercules",

    # Han & Horner
    "HHReaper",
    "HHHellion",
    "HHWidowMine",
    "HHWraith",
    "HHBattlecruiser",
    "HHRaven",

    # Mengsk
    "AegisGuard",
    "ShockDivision",
    "Blackhammer",
    "SkyFury",
    "EmperorShadow",
    "PrideOfAugustgrad",

    "HydraliskMengsk",
    "MutaliskMengsk",
    "UltraliskMengsk",
    "ZerglingMengsk",
    "TrooperMengsk",
    "TrooperMengskAA",
    "TrooperMengskFlamethrower",
    "TrooperMengskImproved",

    "BattlecruiserMengsk",
    "ThorMengsk",
    "GhostMengsk",
    "MarauderMengsk",
    "HydraliskMengsk",
    "MutaliskMengsk",
    "UltraliskMengsk",
    "ZerglingMengsk",
    "VikingMengskAssault",
    "VikingMengskFighter",
    "RavenMengsk",
}