'''
Commander Temporary Unit

A unit created by a commander ability, hero ability, summon, calldown, or internal game mechanic that is not part of
the player's persistent army and is expected to disappear automatically after a limited duration or after fulfilling a specific purpose.

Characteristics

A Commander Temporary Unit usually satisfies most of the following:

Spawned by a top-bar ability, calldown, summon, or hero ability.
Has a limited lifetime or purpose.
Not produced from a normal production structure.
Exists primarily as a temporary combat, support, or utility unit.
Automatically despawns, expires, or is removed by game logic.
Is not considered part of the player's standing army.

Rule of thumb

If the unit exists because an ability was activated and is expected to disappear on its own after completing its role,
it is probably a Commander Temporary Unit.
'''

TEMPORARY_UNITS = {
    # Generic
    "ACHeroSpawnPlacement",

    # Nova
    "HealingDrone",
    "NovaACLaserTurret",
    "NovaBoombot",
    "NovaBoombotBurrowed",
    "NovaDefensiveMatrixDrone",
    "NovaGriffinBombingRunStrafer",
    "NovaGriffinBombingRunTargeter",
    "NovaGriffinTransportUnit",
    "NovaReviveBeacon",

    "Marine_BlackOpsSpawnerUnit",
    "Marauder_BlackOpsSpawnerUnit",
    "Ghost_BlackOpsSpawnerUnit",
    "Hellbat_BlackOpsSpawnerUnit",
    "Goliath_BlackOpsSpawnerUnit",
    "SiegeTank_BlackOpsSpawnerUnit",
    "Raven_BlackOpsSpawnerUnit",
    "Banshee_BlackOpsSpawnerUnit",
    "Liberator_BlackOpsSpawnerUnit",

    # Abathur
    "BiomassPickup",
    "BrutaliskPlacement",
    "ToxicNest",
    "ToxicNestBurrowed",
    "AbathurSymbioteBrutalisk",
    "AbathurSymbioteLeviathan",

    # Alarak
    "AlarakReviveBeacon",
    "AlarakSupplicantWarpTrainCreator",
    "AlarakSupplicantWarpTrainDummy",

    # Artanis
    "CommanderPrestigeArtanisOrbitalStrikesArchon",
    "CommanderPrestigeArtanisOrbitalStrikesArchonPrecursor",

    # Dehaka
    "DehakaCoopClone",
    "DehakaPlacement",

    "DehakaDakrunStructure",
    "DehakaGlevigStructure",
    "DehakaMurvarStructure",

    "DehakaGlevigDeepTunnelPlacement",
    "GreaterNydusDestroyerDeepTunnelPlacement",
    "NydusDestroyerDeepTunnelPlacement",

    "EssencePickup",
    "DehakaMurvar",
    "DehakaGlevig",
    "DehakaDakrun",

    # Fenix
    "FenixAdeptShade",
    "FenixTalisAdeptPhaseShift",

    "FenixClolarionBomber",
    "FenixClolarionInterceptor",

    "FenixManaDummy1",
    "FenixManaDummy2",
    "FenixManaDummy3",

    "SentryFenixPhasing",

    # Han & Horner
    "HHBomber",
    "HHGriffon",

    "HHMagneticMine",
    "HHMagneticMinePrep",

    "HornerAirFleetStrafer",
    "HornerAirFleetTargeter",

    "HHD8CenterCluster",
    "HHD8CenterClusterUpgrade",
    "HHD8ClusterBomb",
    "HHD8SingleCluster",

    "HHScrapPickup",

    # Kerrigan
    "KerriganReviveCocoon",

    # Mengsk
    "CommanderPrestigeMengskTrooperBoom",
    "TrooperMengskWeaponAAPickup",
    "TrooperMengskWeaponFlamethrowerPickup",
    "TrooperMengskWeaponImprovedPickup",


    # Raynor
    "HyperionAdvancedPointDefenseDrone",

    # Stetmann
    "PowerTowerStetmann",
    "PowerTowerStetmannDeactivated",

    # Stukov
    "ALEKSANDERCRASH_PLACEHOLDER",
    "StukovAleksanderCrashed",
    "StukovAleksander",

    "InfestedCivilianPlaceholder",

    "SICocoonInfestedCivilian",
    "SICocoonInfestedMarine",
    "SICocoonInfestedOverlord",
    "SICocoonInfestedSCV",

    "SICocoonInfestedBanshee",
    "SICocoonInfestedDiamondBack",
    "SICocoonInfestedLiberator",
    "SICocoonInfestedSiegeTank",

    "StukovInfestBroodling",
    "StukovInfestedSiegeTankDeepTunnelPlacementUnit",
    "StukovApocalisk",

    # Swann
    "PerditionTurret",
    "PerditionTurretUnderground",

    "KelMorianGrenadeTurret",
    "KelMorianMissileTurret",

    "ThorWreckageSwann",
    "SiegeTankWreckage",

    # Tychus
    "TychusMedicTransportUnit",

    "TychusSCVAutoTurret",
    "TychusWarhoundAutoTurret",

    "TychusMarauderHealingWard",

    "TychusOdinPrecursor",

    # Karax
    "SOAPurifierBeamUnit",
    "SOAThermalLanceTargeter",

    "SOAPylonPowerUnit",
    "SOAPylonPowerAllyUnit",

    "CarrierRepairDrone",

    # Vorazun
    "DarkPylon",
    "OracleStasisTrap",
    "VorazunShadowGuard",

    # Zagara
    "BanelingCocoon",
    "BroodlingEscort",
    "TorrasqueChrysalis",
    "ZagaraReviveCocoon",

    # Zeratul
    "CommanderPrestigeZeratulTornadoesTornado",
    "ProphecyArtifactHintUnit",
    "ProphecyCamera",
    "ZeratulACArtifact",
    "ZeratulArtifactPickup1",
    "ZeratulArtifactPickup2",
    "ZeratulArtifactPickup3",
    "ZeratulArtifactPickupUnlimited",
    "ZeratulCoopReviveBeacon",
    "ZeratulDisruptorPhased",
    "ZeratulStalkerGhost",
    "HotSSplitterlingBig"
    "HotSSplitterlingMedium"
    "PurificationOrbSmall",
    "ZeratulSuppressionCrystal",
    "ZeratulXelNagaChargedCrystalCyan",
    "ZeratulSummonKarass",

    # Morph / helper entities
    "Egg",
    "EggStetmann",
    "OverlordCocoon",
    "DevourerCocoonMP",

    "Larva",
    "LarvaStetmann",

    "CreepTumor",
    "CreepTumorBurrowed",
    "CreepTumorQueenNoCreep",
    "CreepTumorUsed",

    "SNARE_PLACEHOLDER",
}