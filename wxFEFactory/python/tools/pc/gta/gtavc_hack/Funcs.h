/*thiscall*/ void CAutomobile::AddDamagedVehicleParticles(void) 0x5920A0
/*thiscall*/ bool CAutomobile::AddWheelDirtAndWater(CColPoint &colPoint, uint) 0x591B90
/*thiscall*/ void CAutomobile::BlowUpCarsInPath(void) 0x5863D0
/*thiscall*/ void CAutomobile::CAutomobile(int modelIndex, uchar) 0x59E620
/*thiscall*/ void CAutomobile::ClearHeliOrientation(void) 0x59B490
/*thiscall*/ void CAutomobile::CloseBoot(void) 0x585D80
/*thiscall*/ void CAutomobile::DoDriveByShootings(void) 0x5C97B0
/*thiscall*/ void CAutomobile::DoHoverSuspensionRatios(void) 0x585B60
/*thiscall*/ void CAutomobile::FireTruckControl(float) 0x57AB30
/*thiscall*/ void CAutomobile::Fix(void) 0x588530
/*thiscall*/ bool CAutomobile::HasCarStoppedBecauseOfLight(void) 0x435570
/*thiscall*/ void CAutomobile::HydraulicControl(void) 0x59D260
/*thiscall*/ CPed* CAutomobile::KnockPedOutCar(eWeaponType weapon, ushort, CPed * ped) 0x585F20
/*thiscall*/ void CAutomobile::PlaceOnRoadProperly(void) 0x586110
/*thiscall*/ void CAutomobile::PlayHornIfNecessary(void) 0x5881F0
/*thiscall*/ void CAutomobile::PopBoot(void) 0x585E60
/*thiscall*/ void CAutomobile::PopBootUsingPhysics(void) 0x585E20
/*thiscall*/ void CAutomobile::ProcessAutoBusDoors(void) 0x586EC0
/*thiscall*/ void CAutomobile::ProcessBuoyancy(void) 0x599B30
/*thiscall*/ void CAutomobile::ProcessSwingingDoor(int nodeIndex, eDoors door) 0x592C40
/*thiscall*/ bool CAutomobile::RcbanditCheck1CarWheels(CPtrList &ptrlist) 0x5878E0
/*thiscall*/ bool CAutomobile::RcbanditCheckHitWheels(void) 0x587B40
/*thiscall*/ void CAutomobile::ReduceHornCounter(void) 0x59AA90
/*thiscall*/ CObject* CAutomobile::RemoveBonnetInPedCollision(void) 0x592BA0
/*thiscall*/ void CAutomobile::ScanForCrimes(void) 0x588120
/*thiscall*/ void CAutomobile::SetBumperDamage(int, ePanels panel, bool withoutVisualEffect) 0x59B370
/*thiscall*/ void CAutomobile::SetBusDoorTimer(uint time, uchar) 0x587080
/*thiscall*/ void CAutomobile::SetDoorDamage(int nodeIndex, eDoors door, bool withoutVisualEffect) 0x59B150
/*thiscall*/ void CAutomobile::SetHeliOrientation(float angle) 0x59B4A0
/*thiscall*/ void CAutomobile::SetPanelDamage(int nodeIndex, ePanels panel, bool createWindowGlass) 0x59B2A0
/*thiscall*/ void CAutomobile::SetTaxiLight(bool enable) 0x5882F0
/*thiscall*/ void CAutomobile::SetupDamageAfterLoad(void) 0x588310
/*thiscall*/ void CAutomobile::SetupSuspensionLines(void) 0x59E2B0
/*thiscall*/ CObject* CAutomobile::SpawnFlyingComponent(int nodeIndex, uint collisionType) 0x59AAA0
/*thiscall*/ void CAutomobile::TankControl(void) 0x5864C0
/*thiscall*/ void CAutomobile::TellHeliToGoToCoors(float x, float y, float z, uchar) 0x59B4B0
/*thiscall*/ void CAutomobile::TellPlaneToGoToCoors(float x, float y, float z, uchar) 0x59B420
/*thiscall*/ void CAutomobile::VehicleDamage(float damageIntensity, int) 0x59B550
/*thiscall*/ void CAutomobile::dmgDrawCarCollidingParticles(CVector const& position, float force) 0x59C480
void CBaseModelInfo::Shutdown(void) 0x0
void CBaseModelInfo::DeleteRwObject(void) 0x0
RwObject* CBaseModelInfo::CreateInstance(void) 0x0
RwObject* CBaseModelInfo::CreateInstance(RwMatrixTag *tranform) 0x0
RwObject* CBaseModelInfo::GetRwObject(void) 0x0
void CBaseModelInfo::SetAnimFile(char const* filename) 0x0
void CBaseModelInfo::ConvertAnimFileIndex(void) 0x0
int CBaseModelInfo::GetAnimFileIndex(void) 0x0
/*thiscall*/ void CBaseModelInfo::RemoveRef(void) 0x53F1A0
/*thiscall*/ void CBaseModelInfo::AddRef(void) 0x53F1B0
/*thiscall*/ void CBaseModelInfo::RemoveTexDictionaryRef(void) 0x53F1C0
/*thiscall*/ void CBaseModelInfo::AddTexDictionaryRef(void) 0x53F1D0
/*thiscall*/ void CBaseModelInfo::ClearTexDictionary(void) 0x53F1E0
/*thiscall*/ void CBaseModelInfo::SetTexDictionary(char *txdName) 0x53F1F0
/*thiscall*/ void CBaseModelInfo::Add2dEffect(C2dEffect *effect) 0x53F220
/*thiscall*/ C2dEffect* CBaseModelInfo::Get2dEffect(int effectNumber) 0x53F260
/*thiscall*/ void CBike::AddDamagedVehicleParticles(void) 0x60DD20
/*thiscall*/ bool CBike::AddWheelDirtAndWater(CColPoint &colPoint, uint) 0x60D7F0
/*thiscall*/ void CBike::CBike(int modelIndex, uchar createdBy) 0x615740
/*thiscall*/ void CBike::CalculateLeanMatrix(void) 0x609C90
/*thiscall*/ void CBike::DoDriveByShootings(void) 0x5C91E0
/*thiscall*/ void CBike::Fix(void) 0x609F00
/*thiscall*/ void CBike::GetCorrectedWorldDoorPosition(CVector &out, CVector, CVector) 0x609720
/*thiscall*/ CPed* CBike::KnockOffRider(eWeaponType, uchar, CPed *, bool) 0x613920
/*thiscall*/ void CBike::PlayHornIfNecessary(void) 0x609E10
/*thiscall*/ void CBike::ProcessBuoyancy(void) 0x613540
/*thiscall*/ void CBike::ReduceHornCounter(void) 0x613910
/*thiscall*/ void CBike::SetupSuspensionLines(void) 0x615080
/*thiscall*/ void CBike::VehicleDamage(void) 0x614860
/*thiscall*/ void CBoat::AddWakePoint(CVector posn) 0x59F580
/*thiscall*/ void CBoat::ApplyWaterResistance(void) 0x59FB30
/*thiscall*/ void CBoat::CBoat(int modelIndex, uchar createdBy) 0x5A6470
/*thiscall*/ void CBoat::DoDriveByShootings(void) 0x5C9540
/*cdecl*/ void CBoat::FillBoatList(void) 0x59F360
/*thiscall*/ void CBoat::PruneWakeTrail(void) 0x59F6F0
/*fastcall*/ void CBox::Set(CVector const& sup, CVector const& inf) 0x410910
CTreadable* CBuilding::GetIsATreadable(void) 0x0
/*cdecl*/ bool IsBuildingPointerValid(CBuilding *building) 0x407D30
/*thiscall*/ void CBuilding::ReplaceWithNewModel(int modelIndex) 0x407DB0
/*cdecl*/ void* CBuilding::operator new(uint size) 0x407E10
/*thiscall*/ void CBuilding::CBuilding(void) 0x407E40
/*cdecl*/ void CBulletTraces::AddTrace(CVector * start,CVector * end,float radius,uint time,uchar transparency) 0x573910
/*cdecl*/ void CBulletTraces::AddTrace(CVector * start,CVector * end,int weaponType,CEntity * entity) 0x573D40
/*cdecl*/ void CBulletTraces::Init(void) 0x573E80
/*cdecl*/ void CBulletTraces::Render(void) 0x5729F0
/*cdecl*/ int CCarCtrl::AddToLoadedVehicleArray(int, int, int) 0x4267D0
/*cdecl*/ int CCarCtrl::AddToVehicleArray(int, int) 0x426820
/*cdecl*/ int CCarCtrl::ChooseCarModel(int) 0x426AA0
/*cdecl*/ int CCarCtrl::ChooseCarModelToLoad(int) 0x426A30
/*cdecl*/ int CCarCtrl::ChooseCarRating(CZoneInfo *) 0x426D40
/*cdecl*/ int CCarCtrl::ChooseModel(CZoneInfo *, int *) 0x426B40
/*cdecl*/ int CCarCtrl::ChoosePoliceCarModel(void) 0x426850
/*cdecl*/ void CCarCtrl::ClearInterestingVehicleList(void) 0x41D300
/*cdecl*/ void CCarCtrl::DragCarToPoint(CVehicle *vehicle, CVector *coords) 0x4208B0
/*cdecl*/ float CCarCtrl::FindAngleToWeaveThroughTraffic(CVehicle *vehicle, CPhysical *physical, float, float) 0x423C00
/*cdecl*/ int CCarCtrl::FindLinksToGoWithTheseNodes(CVehicle *vehicle) 0x41CC20
/*cdecl*/ float CCarCtrl::FindMaximumSpeedForThisCarInTraffic(CVehicle *vehicle) 0x425880
/*cdecl*/ char CCarCtrl::FindPathDirection(int, int, int) 0x421DC0
/*cdecl*/ void CCarCtrl::GenerateEmergencyServicesCar(void) 0x41C940
/*cdecl*/ bool CCarCtrl::GenerateOneEmergencyServicesCar(uint model, CVector driveToCoord) 0x41C460
/*cdecl*/ void CCarCtrl::GenerateOneRandomCar(void) 0x426DB0
/*cdecl*/ void CCarCtrl::GenerateRandomCars(void) 0x4292A0
/*cdecl*/ void CCarCtrl::Init(void) 0x4293D0
/*cdecl*/ bool CCarCtrl::IsThisVehicleInteresting(CVehicle *vehicle) 0x41D350
/*cdecl*/ void CCarCtrl::JoinCarWithRoadSystem(CVehicle *vehicle) 0x41D000
/*cdecl*/ bool CCarCtrl::JoinCarWithRoadSystemGotoCoors(CVehicle *vehicle, CVector, bool) 0x41CEB0
/*cdecl*/ bool CCarCtrl::MapCouldMoveInThisArea(float, float) 0x41C2F0
/*cdecl*/ char CCarCtrl::PickNextNodeAccordingStrategy(CVehicle *vehicle) 0x422A10
/*cdecl*/ int CCarCtrl::PickNextNodeRandomly(CVehicle *vehicle) 0x421F70
/*cdecl*/ int CCarCtrl::PickNextNodeToChaseCar(CVehicle *vehicle, float, float, CVehicle *) 0x4213A0
/*cdecl*/ bool CCarCtrl::PickNextNodeToFollowPath(CVehicle *vehicle) 0x420D50
/*cdecl*/ void CCarCtrl::PossiblyRemoveVehicle(CVehicle *vehicle) 0x426030
/*cdecl*/ void CCarCtrl::ReInit(void) 0x429320
/*cdecl*/ void CCarCtrl::RegisterVehicleOfInterest(CVehicle *vehicle) 0x41D370
/*cdecl*/ void CCarCtrl::RemoveCarsIfThePoolGetsFull(void) 0x4264C0
/*cdecl*/ void CCarCtrl::RemoveDistantCars(void) 0x426640
/*cdecl*/ void CCarCtrl::RemoveFromInterestingVehicleList(CVehicle *vehicle) 0x41D320
/*cdecl*/ void CCarCtrl::RemoveFromLoadedVehicleArray(int, int) 0x426740
/*cdecl*/ void CCarCtrl::ScanForPedDanger(CVehicle *vehicle) 0x4255E0
/*cdecl*/ void CCarCtrl::SlowCarDownForCarsSectorList(CPtrList &ptrlist, CVehicle *vehicle, float, float, float, float, float *, float) 0x424B50
/*cdecl*/ void CCarCtrl::SlowCarDownForOtherCar(CEntity *entity, CVehicle *vehicle, float *, float) 0x424780
/*cdecl*/ void CCarCtrl::SlowCarDownForPedsSectorList(CPtrList &ptrlist, CVehicle *vehicle, float, float, float, float, float *, float) 0x424C70
/*cdecl*/ void CCarCtrl::SlowCarOnRailsDownForTrafficAndLights(CVehicle *vehicle) 0x4254C0
/*cdecl*/ void CCarCtrl::SteerAIBoatWithPhysicsAttackingPlayer(CVehicle *vehicle, float *, float *, float *, bool *) 0x41DFA0
/*cdecl*/ void CCarCtrl::SteerAIBoatWithPhysicsHeadingForTarget(CVehicle *vehicle, float, float, float *, float *, float *) 0x41E2D0
/*cdecl*/ void CCarCtrl::SteerAICarBlockingPlayerForwardAndBack(CVehicle *vehicle, float *, float *, float *, bool *) 0x41E520
/*cdecl*/ void CCarCtrl::SteerAICarWithPhysics(CVehicle *vehicle) 0x420580
/*cdecl*/ void CCarCtrl::SteerAICarWithPhysicsFollowPath(CVehicle *vehicle, float *, float *, float *, bool *) 0x41EEE0
/*cdecl*/ void CCarCtrl::SteerAICarWithPhysicsHeadingForTarget(CVehicle *vehicle, CPhysical *, float, float, float *, float *, float *, bool *) 0x41EAB0
/*cdecl*/ void CCarCtrl::SteerAICarWithPhysicsTryingToBlockTarget_Stop(CVehicle *vehicle, float, float, float, float, float *, float *, float *, bool *) 0x41E830
/*cdecl*/ void CCarCtrl::SteerAICarWithPhysics_OnlyMission(CVehicle *vehicle, float *, float *, float *, bool *) 0x41FD10
/*cdecl*/ void CCarCtrl::SteerAIHeliTowardsTargetCoors(CAutomobile *automobile) 0x41D900
/*cdecl*/ void CCarCtrl::SteerAIPlaneTowardsTargetCoors(CAutomobile *automobile) 0x41D410
/*cdecl*/ void CCarCtrl::SwitchVehicleToRealPhysics(CVehicle *vehicle) 0x41D2D0
/*cdecl*/ float CCarCtrl::TestCollisionBetween2MovingRects(CVehicle *vehicle, CVehicle *, float, float, CVector *, CVector *, uchar) 0x424210
/*cdecl*/ void CCarCtrl::UpdateCarCount(CVehicle *vehicle, uchar) 0x41C350
/*cdecl*/ void CCarCtrl::UpdateCarOnRails(CVehicle *vehicle) 0x425BF0
/*cdecl*/ void CCarCtrl::WeaveThroughCarsSectorList(CPtrList &ptrlist, CVehicle *vehicle, CPhysical *, float, float, float, float, float *, float *) 0x423490
/*cdecl*/ void CCarCtrl::WeaveThroughObjectsSectorList(CPtrList &ptrlist, CVehicle *vehicle, float, float, float, float, float *, float *) 0x422B00
/*cdecl*/ void CCarCtrl::WeaveThroughPedsSectorList(CPtrList &ptrlist, CVehicle *vehicle, CPhysical *, float, float, float, float, float *, float *) 0x4230F0
/*thiscall*/ bool CCarGenerator::CheckForBlockage(int modelId) 0x5A6FC0
/*thiscall*/ bool CCarGenerator::CheckIfWithinRangeOfAnyPlayers(void) 0x5A6D00
/*thiscall*/ void CCarGenerator::DoInternalProcessing(void) 0x5A71C0
/*thiscall*/ void CCarGenerator::Process(void) 0x5A7130
/*thiscall*/ unsigned int CCarGenerator::Setup(float x,float y,float z,float angle,int modelId,short primaryColor,short secondaryColor,uchar forceSpawn,uchar
/*thiscall*/ void CCarGenerator::SwitchOff(void) 0x5A7670
/*thiscall*/ void CCarGenerator::SwitchOn(void) 0x5A7650
/*thiscall*/ void CCivilianPed::CCivilianPed(ePedType pedType,uint modelIndex) 0x4EAE00
/*thiscall*/ void CCivilianPed::CivilianAI(void) 0x4E8E20
/*thiscall*/ void CCivilianPed::EnterVacantNearbyCars(void) 0x4E99C0
/*thiscall*/ void CCivilianPed::UseNearbyAttractors(void) 0x4E9E90
/*cdecl*/ WORD CClock::GetGameClockMinutesUntil(BYTE hours, BYTE minutes) 0x487130
/*cdecl*/ bool CClock::GetIsTimeInRange(BYTE hourA, BYTE hourB) 0x4870F0
/*cdecl*/ void CClock::Initialise(DWORD milisecondsPerGameMinute) 0x4871B0
/*cdecl*/ void CClock::RestoreClock(void) 0x486FB0
/*cdecl*/ void CClock::SetGameClock(BYTE hours, BYTE minutes) 0x487160
/*cdecl*/ void CClock::StoreClock(void) 0x486FE0
/*cdecl*/ void CClouds::Init(void) 0x540FB0
/*cdecl*/ void CClouds::Render(void) 0x53FC50
/*cdecl*/ void CClouds::RenderBackground(short,short,short,short,short,short,short) 0x53F650
/*cdecl*/ void CClouds::RenderHorizon(void) 0x53F380
/*cdecl*/ void CClouds::Shutdown(void) 0x540F40
/*cdecl*/ void CClouds::Update(void) 0x540E90
void CClumpModelInfo::SetClump(RpClump *) 0x6980B8
/*cdecl*/ void CClumpModelInfo::FillFrameArray(RpClump *clump, RwFrame **frames) 0x541100
/*cdecl*/ RwFrame* CClumpModelInfo::FindFrameFromIdCB(RwFrame *frame, void *searchData) 0x541160
/*cdecl*/ RwFrame* CClumpModelInfo::FindFrameFromNameCB(RwFrame *frame, void *searchData) 0x5411E0
/*cdecl*/ RwFrame* CClumpModelInfo::FindFrameFromNameWithoutIdCB(RwFrame *frame, void *searchData) 0x541190
/*cdecl*/ RwFrame* CClumpModelInfo::GetFrameFromId(RpClump *clump, int id) 0x541120
/*cdecl*/ void CClumpModelInfo::SetAtomicRendererCB(RpAtomic *atomic, void *renderFunc) 0x5412A0
/*thiscall*/ void CClumpModelInfo::SetFrameIds(RwObjectNameIdAssocation *data) 0x541090
/*thiscall*/ void CColBox::Set(CVector const& sup, CVector const& inf, uchar material, uchar flags) 0x4108D0
/*thiscall*/ void CColBox::operator=(CColBox const& right) 0x410890
/*thiscall*/ void CColLine::CColLine(CVector const& start, CVector const& end) 0x410940
/*thiscall*/ void CColModel::CColModel(void) 0x417120
/*thiscall*/ void CColModel::CalculateTrianglePlanes(void) 0x416AE0
/*thiscall*/ int CColModel::GetLinkPtr(void) 0x416A70
/*thiscall*/ int CColModel::GetTrianglePoint(CVector &, int) 0x416B40
/*thiscall*/ void CColModel::RemoveCollisionVolumes(void) 0x4169B0
/*thiscall*/ void CColModel::RemoveTrianglePlanes(void) 0x416AB0
/*cdecl*/ void CColModel::operator delete(void * data) 0x4170E0
/*cdecl*/ void* CColModel::operator new(uint size) 0x417100
/*thiscall*/ void CColModel::operator=(CColModel const&) 0x416B80
/*thiscall*/ void CColPoint::operator=(CColPoint const&) 0x417210
/*thiscall*/ bool CColSphere::IntersectRay(CVector const& rayStart, CVector const& rayEnd, CVector& intPoint1, CVector& intPoint2) 0x417260
/*thiscall*/ void CColSphere::Set(float radius, CVector const& center, uchar material, uchar flags) 0x4173A0
/*thiscall*/ void CCopPed::ArrestPlayer(void) 0x4EB470
/*thiscall*/ void CCopPed::CCopPed(eCopType copType, int) 0x4ED720
/*thiscall*/ void CCopPed::ClearPursuit(void) 0x4EB770
/*thiscall*/ void CCopPed::CopAI(void) 0x4EBC10
/*thiscall*/ void CCopPed::ProcessHeliSwat(void) 0x4EB280
/*thiscall*/ void CCopPed::ProcessStingerCop(void) 0x4EB010
/*thiscall*/ int CCopPed::ScanForCrimes(void) 0x4EBAD0
/*thiscall*/ void CCopPed::SetArrestPlayer(CPed * ped) 0x4EB5F0
/*thiscall*/ void CCopPed::SetPursuit(bool) 0x4EB9C0
/*thiscall*/ void CCutsceneObject::CCutsceneObject(void) 0x4E04D0
/*thiscall*/ void CCutsceneObject::CreateShadow(void) 0x4E03E0
/*thiscall*/ bool CDamageManager::ApplyDamage(tComponent component, float intensity, float) 0x5A9650
/*thiscall*/ void CDamageManager::FuckCarCompletely(void) 0x5A9600
/*thiscall*/ bool CDamageManager::GetComponentGroup(tComponent component, tComponentGroup* group, uchar *damageCompId) 0x5A98D0
/*thiscall*/ uint CDamageManager::GetDoorStatus(eDoors door) 0x5A9810
/*thiscall*/ uint CDamageManager::GetEngineStatus(void) 0x5A97E0
/*thiscall*/ uint CDamageManager::GetLightStatus(eLights light) 0x5A9870
/*thiscall*/ uint CDamageManager::GetPanelStatus(ePanels panel) 0x5A9850
/*thiscall*/ uint CDamageManager::GetWheelStatus(int wheel) 0x5A9830
/*thiscall*/ bool CDamageManager::ProgressPanelDamage(uchar panel) 0x5A9790
/*thiscall*/ void CDamageManager::ResetDamageStatus(void) 0x5A9890
/*thiscall*/ void CDamageManager::SetDoorStatus(eDoors door, uint status) 0x5A9820
/*thiscall*/ void CDamageManager::SetEngineStatus(uint status) 0x5A97F0
/*thiscall*/ void CDamageManager::SetWheelStatus(int wheel, uint status) 0x5A9840
/*cdecl*/ void CDarkel::DealWithWeaponChangeAtEndOfFrenzy(void) 0x429910
/*cdecl*/ void CDarkel::DrawMessages(void) 0x429FE0
/*cdecl*/ bool CDarkel::FrenzyOnGoing(void) 0x429FC0
/*cdecl*/ void CDarkel::Init(void) 0x42A7A0
/*cdecl*/ __int16 CDarkel::QueryModelsKilledByPlayer(int) 0x429AF0
/*cdecl*/ __int16 CDarkel::ReadStatus(void) 0x429FD0
/*cdecl*/ int CDarkel::RegisterCarBlownUpByPlayer(CVehicle *vehicle) 0x429DF0
/*cdecl*/ void CDarkel::RegisterKillByPlayer(CPed *ped, eWeaponType weaponType, bool) 0x429E90
/*cdecl*/ void CDarkel::RegisterKillNotByPlayer(CPed *, eWeaponType weaponType) 0x429E80
/*cdecl*/ void CDarkel::ResetModelsKilledByPlayer(void) 0x429B00
/*cdecl*/ void CDarkel::ResetOnPlayerDeath(void) 0x429F90
/*cdecl*/ void CDarkel::StartFrenzy(eWeaponType weaponType, int, ushort, int, ushort *, int, int, int, bool, bool) 0x429B60
/*cdecl*/ void CDarkel::Update(void) 0x42A650
float CDraw::ms_fFOV 0x696658
float CDraw::ms_fAspectRatio 0x94DD38
float CDraw::ms_fFarClipZ 0xA10678
float CDraw::ms_fNearClipZ 0x978534
float CDraw::ms_fLODDistance 0x97F274
unsigned char CDraw::FadeRed 0xA10B4B
unsigned char CDraw::FadeGreen 0xA10B21
unsigned char CDraw::FadeBlue 0xA10AED
unsigned char CDraw::FadeValue 0xA10B16
/*cdecl*/ void CDraw::CalculateAspectRatio(void) 0x54A270
/*cdecl*/ void CDraw::SetFOV(float fov) 0x54A2E0
/*cdecl*/ bool IsDummyPointerValid(CDummy *dummy) 0x487460
/*cdecl*/ void* CDummy::operator new(uint size) 0x4877B0
/*thiscall*/ void CDummy::CDummy(void) 0x4877E0
/*thiscall*/ void CDummyObject::CDummyObject(CObject *object) 0x4E05D0
/*thiscall*/ void CDummyObject::CDummyObject(void) 0x4E0640
/*thiscall*/ void CEmergencyPed::CEmergencyPed(uint) 0x4EEB40
/*thiscall*/ void CEmergencyPed::FiremanAI(void) 0x4EDA80
/*thiscall*/ void CEmergencyPed::MedicAI(void) 0x4EDC90
void CEntity::Add(void) 0x0
void CEntity::Remove(void) 0x0
void CEntity::SetModelIndex(uint modelIndex) 0x0
void CEntity::SetModelIndexNoCreate(uint modelIndex) 0x0
void CEntity::CreateRwObject(void) 0x0
void CEntity::DeleteRwObject(void) 0x0
CRect CEntity::GetBoundRect(void) 0x0
void CEntity::ProcessControl(void) 0x0
void CEntity::ProcessCollision(void) 0x0
void CEntity::ProcessShift(void) 0x0
void CEntity::Teleport(CVector posn) 0x0
void CEntity::PreRender(void) 0x0
void CEntity::Render(void) 0x0
bool CEntity::SetupLighting(void) 0x0
void CEntity::RemoveLighting(bool resetWorldColors) 0x0
void CEntity::FlagToDestroyWhenNextProcessed(void) 0x0
/*thiscall*/ void CEntity::SetRwObjectAlpha(int alpha) 0x487990
/*thiscall*/ void CEntity::ModifyMatrixForTreeInWind(void) 0x487A20
/*thiscall*/ void CEntity::SetupBigBuilding(void) 0x487C70
/*thiscall*/ float CEntity::GetDistanceFromCentreOfMassToBaseOfModel(void) 0x487D10
/*thiscall*/ bool CEntity::GetIsOnScreenComplex(void) 0x488250
/*thiscall*/ bool CEntity::GetIsOnScreen(void) 0x4885D0
/*thiscall*/ bool CEntity::IsVisible(void) 0x488720
/*thiscall*/ bool CEntity::GetIsTouching(CVector const&posn,float radius) 0x488740
/*thiscall*/ bool CEntity::HasPreRenderEffects(void) 0x489170
/*thiscall*/ void CEntity::UpdateRpHAnim(void) 0x489330
/*thiscall*/ void CEntity::UpdateRwFrame(void) 0x489360
/*thiscall*/ void CEntity::GetBoundCentre(CVector &out) 0x489380
/*thiscall*/ CVector CEntity::GetBoundCentre(void) 0x4893D0
/*cdecl*/ RpAtomic *AtomicRemoveAnimFromSkinCB(RpAtomic *atomic,void *callbackData) 0x489750
/*thiscall*/ void CEntity::DetachFromRwObject(void) 0x489790
/*thiscall*/ void CEntity::AttachToRwObject(RwObject *rwObject) 0x4897C0
/*thiscall*/ void CEntity::CEntity(void) 0x489910
/*thiscall*/ void CEntity::PruneReferences(void) 0x4C69F0
/*thiscall*/ void CEntity::ResolveReferences(void) 0x4C6A30
/*thiscall*/ void CEntity::CleanUpOldReference(CEntity** pEntity) 0x4C6A80
/*thiscall*/ void CEntity::RegisterReference(CEntity** pEntity) 0x4C6AC0
/*thiscall*/ void CEntity::ProcessLightsForEntity(void) 0x541590
/*thiscall*/ bool CEntity::IsEntityOccluded(void) 0x634AE0
/*cdecl*/ void CEntryInfoNode::operator delete(void *data) 0x489BB0
/*cdecl*/ void* CEntryInfoNode::operator new(uint size) 0x489BD0
/*thiscall*/ void CEntryInfoList::Flush(void) 0x489B60
/*thiscall*/ void CEscalators::AddOne(CVector const&,CVector const&,CVector const&,CVector const&,bool) 0x54B0A0
/*cdecl*/ void CEscalators::Init(void) 0x54B460
/*cdecl*/ void CEscalators::Shutdown(void) 0x54B3A0
/*thiscall*/ void CEscalators::Update(void) 0x54A9B0
/*cdecl*/ int CFileMgr::GetErrorReadWrite(int fileHandle) 0x48DE90
/*cdecl*/ int CFileMgr::CloseFile(int fileHandle) 0x48DEA0
/*cdecl*/ bool CFileMgr::ReadLine(int fileHandle,char *buffer,int maxSize) 0x48DEB0
/*cdecl*/ bool CFileMgr::Seek(int fileHandle,int offset,int origin) 0x48DEE0
/*cdecl*/ int CFileMgr::Write(int fileHandle,char *buffer,int size) 0x48DF30
/*cdecl*/ int CFileMgr::Read(int fileHandle,char *buffer,int size) 0x48DF50
/*cdecl*/ int CFileMgr::OpenFileForWriting(char const*filepath) 0x48DF70
/*cdecl*/ int CFileMgr::OpenFile(char const*filepath,char const*mode) 0x48DF90
/*cdecl*/ int CFileMgr::LoadFile(char const*filepath,uchar *buffer,int size,char const*mode) 0x48DFB0
/*cdecl*/ void CFileMgr::SetDirMyDocuments(void) 0x48E020
/*cdecl*/ void CFileMgr::SetDir(char const*dir) 0x48E030
/*cdecl*/ void CFileMgr::ChangeDir(char const*dir) 0x48E090
/*cdecl*/ void CFileMgr::Initialise(void) 0x48E100
/*cdecl*/ short CFont::character_code(uchar character) 0x54FE50
/*cdecl*/ int CFont::FindNewCharacter(short character) 0x54FE70
/*cdecl*/ void CFont::SetDropShadowPosition(short position) 0x54FF20
/*cdecl*/ void CFont::SetDropColor(CRGBA color) 0x54FF30
/*cdecl*/ void CFont::SetAlphaFade(float fade) 0x54FFC0
/*cdecl*/ void CFont::SetRightJustifyWrap(float wrap) 0x54FFD0
/*cdecl*/ void CFont::SetFontStyle(short style) 0x54FFE0
/*cdecl*/ void CFont::SetPropOn(void) 0x550020
/*cdecl*/ void CFont::SetPropOff(void) 0x550030
/*cdecl*/ void CFont::SetRightJustifyOff(void) 0x550040
/*cdecl*/ void CFont::SetRightJustifyOn(void) 0x550060
/*cdecl*/ void CFont::SetBackGroundOnlyTextOff(void) 0x550080
/*cdecl*/ void CFont::SetBackGroundOnlyTextOn(void) 0x550090
/*cdecl*/ void CFont::SetBackgroundColor(CRGBA color) 0x5500A0
/*cdecl*/ void CFont::SetBackgroundOff(void) 0x5500D0
/*cdecl*/ void CFont::SetBackgroundOn(void) 0x5500E0
/*cdecl*/ void CFont::SetCentreSize(float size) 0x5500F0
/*cdecl*/ void CFont::SetWrapx(float wrap) 0x550100
/*cdecl*/ void CFont::SetCentreOff(void) 0x550110
/*cdecl*/ void CFont::SetCentreOn(void) 0x550120
/*cdecl*/ void CFont::SetJustifyOff(void) 0x550140
/*cdecl*/ void CFont::SetJustifyOn(void) 0x550150
/*cdecl*/ void CFont::SetColor(CRGBA color) 0x550170
/*cdecl*/ void CFont::SetSlant(float slant) 0x550200
/*cdecl*/ void CFont::SetSlantRefPoint(float x,float y) 0x550210
/*cdecl*/ void CFont::SetScale(float width,float height) 0x550230
/*cdecl*/ void CFont::DrawFonts(void) 0x550250
/*cdecl*/ void CFont::FilterOutTokensFromString(ushort *str) 0x550260
/*cdecl*/ ushort* CFont::ParseToken(ushort *str) 0x5502D0
/*cdecl*/ ushort* CFont::ParseToken(ushort *str,CRGBA &color,bool &flashing,bool &bold) 0x550510
/*cdecl*/ float CFont::GetStringWidth(ushort *str,bool sentence) 0x550650
/*cdecl*/ void CFont::GetTextRect(CRect *rect_out,float x,float y,ushort *text) 0x550720
/*cdecl*/ int CFont::GetNumberLines(float x,float y,ushort *text) 0x550C70
/*cdecl*/ void CFont::PrintString(float x,float y,ushort *text) 0x551040
/*cdecl*/ void CFont::PrintStringFromBottom(float x,float y,ushort *text) 0x551620
/*cdecl*/ void CFont::PrintString(float x,float y,uint,ushort *,ushort *,float) 0x5516C0
/*cdecl*/ void CFont::RenderFontBuffer(void) 0x551A30
/*cdecl*/ void CFont::PrintChar(float x,float y,short character) 0x551E70
/*cdecl*/ void CFont::InitPerFrame(void) 0x5522B0
/*cdecl*/ void CFont::Shutdown(void) 0x5522E0
/*cdecl*/ void CFont::Initialise(void) 0x552310
/*cdecl*/ void UnicodeMakeUpperCase(ushort *str_out,ushort const*str_in) 0x552470
/*cdecl*/ int UnicodeStrlen(ushort const*str) 0x5524B0
/*cdecl*/ void AsciiToUnicode(char const*str_ascii,ushort *str_unicode) 0x552500
/*cdecl*/ bool CGeneral::SolveQuadratic(float a,float b,float c,float &x1,float &x2) 0x4A53D0
/*cdecl*/ int CGeneral::GetNodeHeadingFromVector(float x,float y) 0x4A5450
/*cdecl*/ float CGeneral::GetATanOfXY(float x,float y) 0x4A55E0
/*cdecl*/ float CGeneral::LimitRadianAngle(float angle) 0x4A57F0
/*cdecl*/ float CGeneral::LimitAngle(float angle) 0x4A5890
/*cdecl*/ float CGeneral::GetRadianAngleBetweenPoints(float x1,float y1,float x2,float y2) 0x4A58E0
/*cdecl*/ float CGeneral::GetAngleBetweenPoints(float x1,float y1,float x2,float y2) 0x4A59D0
/*thiscall*/ void cHandlingDataMgr::cHandlingDataMgr(void) 0x5ABDC0
/*thiscall*/ void cHandlingDataMgr::ConvertDataToGameUnits(tHandlingData *handling) 0x5ABAA0
/*thiscall*/ int cHandlingDataMgr::FindExactWord(char *line,char *nameTable,int entrySize,int entryCount) 0x5ABD30
/*thiscall*/ tBoatHandlingData* cHandlingDataMgr::GetBoatPointer(uchar handlingId) 0x5ABA40
/*thiscall*/ tFlyingHandlingData* cHandlingDataMgr::GetFlyingPointer(uchar handlingId) 0x5ABA70
/*thiscall*/ int cHandlingDataMgr::GetHandlingId(char const* name) 0x5ABCC0
/*thiscall*/ void cHandlingDataMgr::Initialise(void) 0x5ABA10
/*thiscall*/ void cHandlingDataMgr::LoadHandlingData(void) 0x5AAE20
/*thiscall*/ void CHeli::CHeli(int modelIndex, uchar createdBy) 0x5AF7F0
/*cdecl*/ void CHeli::InitHelis(void) 0x5AD4A0
/*thiscall*/ void CHeli::PreRenderAlways(void) 0x5AF2E0
/*thiscall*/ bool CHeli::SendDownSwat(void) 0x5ABE20
/*thiscall*/ CObject* CHeli::SpawnFlyingComponent(int nodeIndex) 0x5AC1E0
/*cdecl*/ bool CHeli::SpecialHeliPreRender(void) 0x5AC500
/*cdecl*/ bool CHeli::TestBulletCollision(CVector *, CVector *, CVector *, int) 0x5AC6C0
/*cdecl*/ bool CHeli::TestRocketCollision(CVector *) 0x5AC9A0
/*cdecl*/ bool CHeli::TestSniperCollision(CVector* origin, CVector* target) 0x5AC520
/*cdecl*/ void CHeli::UpdateHelis(void) 0x5ACDA0
/*cdecl*/ void GenerateHeli(bool enable) 0x5ACB30
/*cdecl*/ void StartCatalinaFlyBy(void) 0x5ACAF0
/*cdecl*/ RwObject* GetHeliAtomicObjectCB(RwObject* object, void* data) 0x5AC4E0
/*cdecl*/ void CHud::Draw(void) 0x557320
/*cdecl*/ void CHud::DrawAfterFade(void) 0x5566E0
/*cdecl*/ float CHud::DrawFadeState(DRAW_FADE_STATE fadeState,int) 0x55BD20
/*cdecl*/ void CHud::GetRidOfAllHudMessages(void) 0x55C200
/*cdecl*/ void CHud::Initialise(void) 0x55C8A0
/*cdecl*/ bool CHud::IsHelpMessageBeingDisplayed(void) 0x55BFB0
/*cdecl*/ void CHud::ReInitialise(void) 0x55C440
/*cdecl*/ void CHud::ResetWastedText(void) 0x556570
/*cdecl*/ void CHud::SetBigMessage(ushort *text,ushort style) 0x5565B0
/*cdecl*/ void CHud::SetHelpMessage(ushort *text, bool quickMessage, bool permanent, bool addToBrief) 0x55BFC0
/*cdecl*/ void CHud::SetMessage(ushort *text) 0x5566A0
/*cdecl*/ void CHud::SetPagerMessage(ushort *text) 0x5565A0
/*cdecl*/ void CHud::SetVehicleName(ushort *text) 0x55BFA0
/*cdecl*/ void CHud::SetZoneName(ushort *text) 0x55C1F0
/*cdecl*/ void CHud::Shutdown(void) 0x55C7F0
/*cdecl*/ void CIniFile::LoadIniFile(void) 0x56D070
/*cdecl*/ CMatrix operator*(CMatrix const&a,CMatrix const&b) 0x4DE6C0
/*cdecl*/ void Invert(CMatrix const&in,CMatrix&out) 0x4DE870
/*thiscall*/ void CMatrix::CopyToRwMatrix(RwMatrixTag *rwMatrix) 0x4DE960
/*cdecl*/ CMatrix Invert(CMatrix const&in) 0x4DE9C0
/*thiscall*/ void CMatrix::Reorthogonalise(void) 0x4DEA30
/*thiscall*/ void CMatrix::Rotate(float x,float y,float z) 0x4DEBA0
/*thiscall*/ void CMatrix::RotateZ(float angle) 0x4DEEB0
/*thiscall*/ void CMatrix::RotateY(float angle) 0x4DEFE0
/*thiscall*/ void CMatrix::RotateX(float angle) 0x4DF110
/*thiscall*/ void CMatrix::SetRotate(float x,float y,float z) 0x4DF240
/*thiscall*/ void CMatrix::SetRotateZ(float angle) 0x4DF3B0
/*thiscall*/ void CMatrix::SetRotateY(float angle) 0x4DF450
/*thiscall*/ void CMatrix::SetRotateX(float angle) 0x4DF4F0
/*thiscall*/ void CMatrix::SetRotateZOnly(float angle) 0x4DF590
/*thiscall*/ void CMatrix::SetRotateXOnly(float angle) 0x4DF620
/*thiscall*/ void CMatrix::SetTranslateOnly(float x,float y,float z) 0x4DF6B0
/*thiscall*/ void CMatrix::SetTranslate(float x,float y,float z) 0x4DF6D0
/*thiscall*/ void CMatrix::SetScale(float factor) 0x4DF730
/*thiscall*/ void CMatrix::ResetOrientation(void) 0x4DF780
/*thiscall*/ void CMatrix::SetUnity(void) 0x4DF7C0
/*thiscall*/ void CMatrix::operator+=(CMatrix const&right) 0x4DF820
/*thiscall*/ void CMatrix::CopyOnlyMatrix(CMatrix const&src) 0x4DF8A0
/*thiscall*/ void CMatrix::operator=(CMatrix const&right) 0x4DF8C0
/*thiscall*/ void CMatrix::UpdateRW(void) 0x4DF8F0
/*thiscall*/ void CMatrix::Update(void) 0x4DF970
/*thiscall*/ void CMatrix::Detach(void) 0x4DF9E0
/*thiscall*/ void CMatrix::AttachRW(RwMatrixTag *rwMatrix,bool deleteOnDetach) 0x4DFA00
/*thiscall*/ void CMatrix::Attach(RwMatrixTag *rwMatrix,bool deleteOnDetach) 0x4DFA40
/*thiscall*/ void CMatrix::~CMatrix() 0x4DFAE0
/*thiscall*/ void CMatrix::CMatrix(RwMatrixTag *rwMatrix,bool deleteOnDetach) 0x4DFB00
/*thiscall*/ void CMatrix::CMatrix(CMatrix const&src) 0x4DFBA0
/*cdecl*/ CVector operator*(CMatrix const&m,CVector const&v) 0x4DFF20
/*cdecl*/ CVector Multiply3x3(CVector const&v,CMatrix const&m) 0x4DFFB0
/*cdecl*/ CVector Multiply3x3(CMatrix const&m,CVector const&v) 0x4E0030
/*cdecl*/ CClumpModelInfo* CModelInfo::AddClumpModel(int index) 0x55F640
/*cdecl*/ CPedModelInfo* CModelInfo::AddPedModel(int index) 0x55F580
/*cdecl*/ CSimpleModelInfo* CModelInfo::AddSimpleModel(int index) 0x55F730
/*cdecl*/ CTimeModelInfo* CModelInfo::AddTimeModel(int index) 0x55F6E0
/*cdecl*/ CVehicleModelInfo* CModelInfo::AddVehicleModel(int index) 0x55F5D0
/*cdecl*/ CWeaponModelInfo* CModelInfo::AddWeaponModel(int index) 0x55F690
/*cdecl*/ void* CModelInfo::Get2dEffectStore(void) 0x55F570
/*cdecl*/ CBaseModelInfo* CModelInfo::GetModelInfo(char const* name,int * index) 0x55F7D0
/*cdecl*/ CBaseModelInfo* CModelInfo::GetModelInfo(char const* name,int minIndex,int maxInedx) 0x55F780
/*cdecl*/ void CModelInfo::Initialise(void) 0x55FA40
/*cdecl*/ bool CModelInfo::IsBikeModel(int index) 0x55F4E0
/*cdecl*/ bool CModelInfo::IsBoatModel(int index) 0x55F540
/*cdecl*/ bool CModelInfo::IsCarModel(int index) 0x55F510
/*cdecl*/ void CModelInfo::ShutDown(void) 0x55F820
/*thiscall*/ void CObject::CObject(CDummyObject * dummyObject) 0x4E40F0
/*thiscall*/ void CObject::CObject(int,bool) 0x4E41B0
/*thiscall*/ void CObject::CObject(void) 0x4E4220
/*thiscall*/ bool CObject::CanBeDeleted(void) 0x4E3E20
/*cdecl*/ void CObject::DeleteAllMissionObjects(void) 0x4E0820
/*cdecl*/ void CObject::DeleteAllTempObjects(void) 0x4E08A0
/*cdecl*/ void CObject::DeleteAllTempObjectsInArea(CVector point, float radius) 0x4E0720
/*thiscall*/ void CObject::Init(void) 0x4E3E50
/*thiscall*/ void CObject::ObjectDamage(float damage) 0x4E0990
/*thiscall*/ void CObject::RefModelInfo(int modelIndex) 0x4E0970
/*cdecl*/ void CObject::operator delete(void * data) 0x4E4030
/*cdecl*/ void* CObject::operator new(uint size) 0x4E4070
/*cdecl*/ void CObject::operator new(uint size, int) 0x4E4050
/*cdecl*/ float FindPlayerHeading(void) 0x4BBF70;
/*cdecl*/ CVector& FindPlayerCentreOfWorld_NoSniperShift(void) 0x4BC020;
/*cdecl*/ CVector& FindPlayerCentreOfWorld(int playerId) 0x4BC0A0;
/*cdecl*/ CPed* FindPlayerPed(void) 0x4BC120;
/*cdecl*/ CTrain* FindPlayerTrain(void) 0x4BC140;
/*cdecl*/ CEntity* FindPlayerEntity(void) 0x4BC1B0;
/*cdecl*/ CVehicle* FindPlayerVehicle(void) 0x4BC1E0;
/*cdecl*/ CVector& FindPlayerSpeed(void) 0x4BC210;
/*cdecl*/ CVector& FindPlayerCoors(void) 0x4BC240;
/*cdecl*/ RwTexture* GetFirstTexture(RwTexDictionary *texDictionary) 0x57F900
/*cdecl*/ RwObject* GetFirstObject(RwFrame *frame) 0x57F940
/*cdecl*/ RpAtomic* GetFirstAtomic(RpClump *clump) 0x57F980
/*cdecl*/ void SetAmbientColours(RwRGBAReal *colours) 0x57FAD0
/*cdecl*/ void SetAmbientColoursForPedsCarsAndObjects(void) 0x57FAF0
/*cdecl*/ void SetAmbientColours(void) 0x57FB10
/*cdecl*/ void SetFullAmbient(void) 0x57FB30
/*cdecl*/ void ActivateDirectional(void) 0x57FB50
/*cdecl*/ void DeActivateDirectional(void) 0x57FB60
/*cdecl*/ void ReSetAmbientAndDirectionalColours(void) 0x57FB70
/*cdecl*/ void SetBrightMarkerColours(float power) 0x57FBA0
/*cdecl*/ void SetAmbientAndDirectionalColours(float power) 0x57FC50
/*cdecl*/ void RemoveExtraDirectionalLights(RpWorld *world) 0x57FCD0
/*cdecl*/ void AddAnExtraDirectionalLight(RpWorld *world,float x,float y,float z,float red,float green,float blue) 0x57FD00
/*cdecl*/ void WorldReplaceNormalLightsWithScorched(RpWorld *world,float intensity) 0x57FE40
/*cdecl*/ RpWorld* LightsDestroy(RpWorld *world) 0x57FE80
/*cdecl*/ RpWorld* LightsCreate(RpWorld *world) 0x57FF50
/*cdecl*/ void SetLightsWithTimeOfDayColour(RpWorld *world) 0x5800F0
/*cdecl*/ RpAtomic* GetCurrentAtomicObjectCB(RwObject *object, void *data) 0x59F1E0
/*thiscall*/ void COnscreenTimer::AddClock(uint, char *, bool) 0x434B30
/*thiscall*/ void COnscreenTimer::AddCounter(uint, ushort, char *, ushort) 0x434AE0
/*thiscall*/ void COnscreenTimer::ClearClock(uint) 0x434AA0
/*thiscall*/ void COnscreenTimer::ClearCounter(uint) 0x434A60
/*thiscall*/ void COnscreenTimer::Init(void) 0x434CE0
/*thiscall*/ void COnscreenTimer::Process(void) 0x434B90
/*thiscall*/ void COnscreenTimer::ProcessForDisplay(void) 0x434BD0
/*thiscall*/ void COnscreenTimerEntry::Process(void) 0x434DE0
void CPed::SetMoveAnim(void) 0x50CD50
/*thiscall*/ int CPed::AddInCarAnims(CVehicle *vehicle,bool) 0x512520
/*thiscall*/ void CPed::AddWeaponModel(int modelIndex) 0x4FFE40
/*thiscall*/ char CPed::AimGun(void) 0x50B2C0
/*thiscall*/ void CPed::AnswerMobile(void) 0x4F5710
/*thiscall*/ CEntity* CPed::AttachPedToEntity(CEntity *entity,CVector offset,ushort position,float angle,eWeaponType weaponType) 0x4EF490
/*thiscall*/ uint CPed::Attack(void) 0x52B070
/*thiscall*/ void CPed::Avoid(void) 0x4FA2E0
/*thiscall*/ int CPed::BeingDraggedFromCar(void) 0x518250
/*thiscall*/ void CPed::BuildPedLists(void) 0x50D4B0
/*thiscall*/ void CPed::BuyIceCream(void) 0x4F10D0
/*thiscall*/ void CPed::CalculateNewOrientation(void) 0x509F80
/*thiscall*/ void CPed::CalculateNewVelocity(void) 0x50A640
/*thiscall*/ bool CPed::CanBeDamagedByThisGangMember(CPed* ped) 0x50F130
/*thiscall*/ bool CPed::CanBeDeleted(void) 0x4FFEF0
/*thiscall*/ bool CPed::CanBeDeletedEvenInVehicle(void) 0x4FFEC0
/*thiscall*/ bool CPed::CanPedDriveOff(void) 0x4EFC90
/*thiscall*/ bool CPed::CanPedJumpThis(CEntity *entity,CVector *) 0x4F0590
/*thiscall*/ bool CPed::CanSeeEntity(CEntity *entity,float limitAngle) 0x51C870
/*thiscall*/ bool CPed::CanSetPedState(void) 0x5018D0
/*thiscall*/ bool CPed::CanStrafeOrMouseControl(void) 0x501890
/*thiscall*/ bool CPed::CanWeRunAndFireWithWeapon(void) 0x50B220
/*thiscall*/ uint CPed::Chat(void) 0x4F6050
/*thiscall*/ bool CPed::CheckForExplosions(CVector2D &) 0x4F4950
/*thiscall*/ char CPed::CheckForPointBlankPeds(CPed* ped) 0x52C670
/*thiscall*/ bool CPed::CheckIfInTheAir(void) 0x4FD680
/*thiscall*/ int CPed::CheckThreatValidity(void) 0x50BD00
/*thiscall*/ int CPed::ChooseAttackAI(uchar,bool) 0x529460
/*thiscall*/ int CPed::ChooseAttackPlayer(uchar,bool) 0x528AA0
/*thiscall*/ void CPed::ClearAimFlag(void) 0x50B4A0
/*thiscall*/ void CPed::ClearAll(void) 0x509DF0
/*thiscall*/ void CPed::ClearAnswerMobile(void) 0x4F58C0
/*thiscall*/ void CPed::ClearAttack(void) 0x52D120
/*thiscall*/ void CPed::ClearAttackByRemovingAnim(void) 0x52CF70
/*thiscall*/ void CPed::ClearChat(void) 0x4F5FA0
/*thiscall*/ void CPed::ClearDuck(bool) 0x512A20
/*thiscall*/ void CPed::ClearFollowPath(void) 0x4F7920
/*thiscall*/ void CPed::ClearInvestigateEvent(void) 0x526BA0
/*thiscall*/ void CPed::ClearLeader(void) 0x521670
/*thiscall*/ void CPed::ClearLookFlag(void) 0x50B9C0
/*thiscall*/ void CPed::ClearObjective(void) 0x521720
/*thiscall*/ void CPed::ClearPointGunAt(void) 0x52DBE0
/*thiscall*/ void CPed::ClearSeek(void) 0x4FC450
/*thiscall*/ void CPed::ClearWaitState(void) 0x4F3130
/*thiscall*/ void CPed::ClearWeapons(void) 0x4FF740
/*thiscall*/ void CPed::CollideWithPed(CPed* ped) 0x524920
/*thiscall*/ void CPed::CreateDeadPedMoney(void) 0x43E2C0
/*thiscall*/ void CPed::CreateDeadPedPickupCoors(float *pX,float *pY,float *pZ) 0x43DAC0
/*thiscall*/ void CPed::CreateDeadPedWeaponPickups(void) 0x43DF30
/*thiscall*/ void CPed::DeadPedMakesTyresBloody(void) 0x587700
/*thiscall*/ void CPed::DettachPedFromEntity(void) 0x4EF370
/*thiscall*/ void CPed::Dress(void) 0x4EEFD0
/*thiscall*/ void CPed::DriveVehicle(void) 0x522AA0
/*thiscall*/ void CPed::Duck(void) 0x512A90
/*thiscall*/ void CPed::DuckAndCover(void) 0x513340
/*thiscall*/ void CPed::EndFight(uchar) 0x5289A0
/*thiscall*/ void CPed::EnterCar(void) 0x517BA0
/*thiscall*/ void CPed::ExitCar(void) 0x516960
/*thiscall*/ bool CPed::FacePhone(void) 0x4F5CA0
/*thiscall*/ void CPed::Fall(void) 0x4FD740
/*thiscall*/ void CPed::Fight(void) 0x529A00
/*thiscall*/ void CPed::FightHitPed(CPed* ped,CVector &,CVector &,short) 0x527800
/*thiscall*/ void CPed::FightStrike(CVector &,bool) 0x5282E0
/*thiscall*/ bool CPed::FindBestCoordsFromNodes(CVector,CVector*) 0x513DF0
/*thiscall*/ void CPed::Flee(void) 0x4FB130
/*thiscall*/ __int16 CPed::FollowPath(void) 0x4F76C0
/*thiscall*/ int CPed::GetFormationPosition(void) 0x519E30
/*thiscall*/ int CPed::GetLocalDirection(CVector2D const&) 0x5035F0
/*cdecl*/ int CPed::GetLocalPositionToOpenCarDoor(CVehicle *vehicle,uint,float) 0x512D10
/*thiscall*/ int CPed::GetNearestDoor(CVehicle *vehicle,CVector &position) 0x5160E0
/*thiscall*/ bool CPed::GetNearestPassengerDoor(CVehicle *vehicle,CVector &position) 0x515CE0
/*thiscall*/ bool CPed::GetNearestTrainDoor(CVehicle *vehicle,CVector &position) 0x514A70
/*thiscall*/ bool CPed::GetNearestTrainPedPosition(CVehicle *vehicle,CVector &position) 0x514650
/*thiscall*/ int CPed::GetNextPointOnRoute(void) 0x51C9E0
/*cdecl*/ int CPed::GetPositionToOpenCarDoor(CVehicle *vehicle,uint) 0x5164D0
/*cdecl*/ int CPed::GetPositionToOpenCarDoor(CVehicle *vehicle,uint,float) 0x513080
/*thiscall*/ int CPed::GetWeaponSlot(eWeaponType weaponType) 0x4FFA10
/*thiscall*/ void CPed::GiveDelayedWeapon(eWeaponType weaponType,uint ammo) 0x4FFC30
/*thiscall*/ void CPed::GiveWeapon(eWeaponType weaponType,uint ammo,bool likeUnused) 0x4FFA30
/*thiscall*/ void CPed::GrantAmmo(eWeaponType weaponType,uint ammo) 0x4FF840
/*thiscall*/ bool CPed::HasAttractor(void) 0x4EF8A0
/*thiscall*/ bool CPed::HaveReachedNextPointOnRoute(float) 0x51C970
/*thiscall*/ void CPed::Idle(void) 0x4FDEB0
/*thiscall*/ void CPed::InTheAir(void) 0x4FD4D0
/*thiscall*/ void CPed::InflictDamage(void *,eWeaponType weaponType,float,ePedPieceTypes,uchar) 0x525B20
/*thiscall*/ void CPed::InformMyGangOfAttack(CEntity *entity) 0x512950
/*cdecl*/ void CPed::Initialise(void) 0x50D9F0
/*thiscall*/ void CPed::InvestigateEvent(void) 0x526C60
/*thiscall*/ bool CPed::IsGangMember(void) 0x4F4910
/*thiscall*/ bool CPed::IsPedDoingDriveByShooting(void) 0x5C84D0
/*thiscall*/ bool CPed::IsPedHeadAbovePos(float zPos) 0x525960
/*thiscall*/ bool CPed::IsPedInControl(void) 0x501950
/*thiscall*/ bool CPed::IsPedShootable(void) 0x501930
/*thiscall*/ bool CPed::IsPlayer(void) 0x4F4930
/*thiscall*/ bool CPed::IsPointerValid(void) 0x4F4860
/*thiscall*/ bool CPed::IsRoomToBeCarJacked(void) 0x512670
/*thiscall*/ void CPed::KillCharOnFootArmed(CVector &,CVector &,CVector &) 0x50FFC0
/*thiscall*/ void CPed::KillCharOnFootMelee(CVector &,CVector &,CVector &) 0x50F170
/*thiscall*/ void CPed::KillPedWithCar(CVehicle *vehicle,float) 0x523CD0
/*thiscall*/ void CPed::LineUpPedWithCar(uint) 0x518AD0
/*cdecl*/ void CPed::LoadFightData(void) 0x527570
/*thiscall*/ void CPed::LookForInterestingNodes(void) 0x4F3540
/*thiscall*/ void CPed::LookForSexyCars(void) 0x4F3EB0
/*thiscall*/ void CPed::LookForSexyPeds(void) 0x4F4090
/*thiscall*/ bool CPed::MakePhonecall(void) 0x4F5B40
/*thiscall*/ void CPed::MakeTyresMuddySectorList(CPtrList &ptrList) 0x5870D0
/*thiscall*/ void CPed::MoveHeadToLook(void) 0x50B700
/*thiscall*/ void CPed::Mug(void) 0x4FCD30
/*thiscall*/ bool CPed::OurPedCanSeeThisOne(CEntity *entity,bool) 0x50D360
/*thiscall*/ void CPed::Pause(void) 0x4FDE80
/*thiscall*/ void CPed::PedShuffle(void) 0x51A2F0
/*thiscall*/ bool CPed::PlacePedOnDryLand(void) 0x5256A0
/*thiscall*/ void CPed::PlayFootSteps(void) 0x503680
/*thiscall*/ void CPed::PlayHitSound(CPed* ped) 0x528850
/*thiscall*/ __int16 CPed::PointGunAt(void) 0x52DCD0
/*thiscall*/ bool CPed::PositionAnyPedOutOfCollision(void) 0x511840
/*thiscall*/ void CPed::PositionAttachedPed(void) 0x4EF0A0
/*thiscall*/ bool CPed::PositionPedOutOfCollision(void) 0x511B10
/*thiscall*/ bool CPed::PossiblyFindBetterPosToSeekCar(CVector *,CVehicle *vehicle) 0x4F0810
/*thiscall*/ void CPed::ProcessBuoyancy(void) 0x509460
/*thiscall*/ void CPed::ProcessObjective(void) 0x51CA70
/*thiscall*/ void CPed::QuitEnteringCar(void) 0x5179D0
/*thiscall*/ void CPed::ReactToAttack(CEntity *entity) 0x51BDA0
/*thiscall*/ void CPed::ReactToPointGun(CEntity *entity) 0x51C1E0
/*thiscall*/ void CPed::RegisterThreatWithGangPeds(CEntity *entity) 0x514360
/*thiscall*/ void CPed::RemoveDrivebyAnims(void) 0x512480
/*thiscall*/ void CPed::RemoveInCarAnims(bool) 0x512440
/*thiscall*/ void CPed::RemoveWeaponAnims(int likeUnused, float blendDelta) 0x5229B0
/*thiscall*/ void CPed::RemoveWeaponModel(int modelIndex) 0x4FFD80
/*thiscall*/ void CPed::RemoveWeaponWhenEnteringVehicle(void) 0x4FF6A0
/*thiscall*/ void CPed::ReplaceWeaponWhenExitingVehicle(void) 0x4FF5A0
/*thiscall*/ void CPed::RequestDelayedWeapon(void) 0x4FFCE0
/*thiscall*/ void CPed::RestartNonPartialAnims(void) 0x50CCF0
/*thiscall*/ void CPed::RestoreGunPosition(void) 0x50B250
/*thiscall*/ void CPed::RestoreHeadPosition(void) 0x50B650
/*thiscall*/ void CPed::RestoreHeadingRate(void) 0x4F17D0
/*thiscall*/ void CPed::RestorePreviousObjective(void) 0x520FE0
/*thiscall*/ void CPed::RestorePreviousState(void) 0x50C600
/*thiscall*/ void CPed::Say(ushort) 0x5226B0
/*thiscall*/ void CPed::Say(ushort,int) 0x4EEFA0
/*thiscall*/ void CPed::ScanForDelayedResponseThreats(void) 0x50BD80
/*thiscall*/ void CPed::ScanForInterestingStuff(void) 0x50AD50
/*thiscall*/ void CPed::ScanForThreats(void) 0x50BE00
/*thiscall*/ bool CPed::Seek(void) 0x4FBD00
/*thiscall*/ void CPed::SeekBoatPosition(void) 0x512740
/*thiscall*/ void CPed::SeekCar(void) 0x4F4AD0
/*thiscall*/ void CPed::SeekFollowingPath(void) 0x4FA1C0
/*thiscall*/ bool CPed::SelectGunIfArmed(void) 0x51C800
/*thiscall*/ void CPed::ServiceTalking(void) 0x522850
/*thiscall*/ bool CPed::ServiceTalkingWhenDead(void) 0x522990
/*thiscall*/ void CPed::SetAimFlag(CEntity *aimingTo) 0x50B510
/*thiscall*/ void CPed::SetAimFlag(float heading) 0x50B5B0
/*thiscall*/ void CPed::SetAmmo(eWeaponType weaponType, uint ammo) 0x4FF780
/*cdecl*/ void CPed::SetAnimOffsetForEnterOrExitVehicle(void) 0x5155E0
/*thiscall*/ void CPed::SetAnswerMobile(void) 0x4F59C0
/*thiscall*/ void CPed::SetAttack(CEntity *entity) 0x52D1C0
/*thiscall*/ void CPed::SetAttackTimer(uint time) 0x4FCAB0
/*thiscall*/ void CPed::SetBeingDraggedFromCar(CVehicle *vehicle,uint,bool) 0x518430
/*thiscall*/ void CPed::SetCarJack(CVehicle *vehicle) 0x5188A0
/*thiscall*/ void CPed::SetCarJack_AllClear(CVehicle *vehicle,uint,uint) 0x518690
/*thiscall*/ void CPed::SetChat(CEntity *entity,uint) 0x4F6220
/*thiscall*/ void CPed::SetCurrentWeapon(eWeaponType weaponType) 0x4FF8E0
/*thiscall*/ void CPed::SetCurrentWeapon(int slot) 0x4FF900
/*thiscall*/ void CPed::SetDead(void) 0x4F6430
/*thiscall*/ void CPed::SetDie(AnimationId,float,float) 0x4F65C0
/*thiscall*/ void CPed::SetDirectionToWalkAroundObject(CEntity *entity) 0x5019A0
/*thiscall*/ void CPed::SetDirectionToWalkAroundVehicle(CVehicle *vehicle) 0x5035B0
/*thiscall*/ void CPed::SetDuck(uint,bool) 0x512C10
/*thiscall*/ void CPed::SetEnterCar(CVehicle *vehicle,uint) 0x518080
/*thiscall*/ void CPed::SetEnterCar_AllClear(CVehicle *vehicle,uint,uint) 0x517DE0
/*thiscall*/ void CPed::SetEvasiveDive(CPhysical *,uchar) 0x4F6A20
/*thiscall*/ void CPed::SetEvasiveStep(CPhysical *,uchar) 0x4F7170
/*thiscall*/ void CPed::SetExitBoat(CVehicle *boat) 0x517670
/*thiscall*/ void CPed::SetExitCar(CVehicle *vehicle,uint) 0x516C60
/*thiscall*/ void CPed::SetFall(int,AnimationId,uchar) 0x4FD9F0
/*thiscall*/ void CPed::SetFlee(CEntity *,int) 0x4FB820
/*thiscall*/ void CPed::SetFlee(CVector2D const&,int) 0x4FBA90
/*thiscall*/ void CPed::SetFollowPath(CVector const&,float,eMoveState,CEntity *,CEntity *,int) 0x4F9F60
/*thiscall*/ bool CPed::SetFollowPathDynamic(void) 0x4F7990
/*thiscall*/ bool CPed::SetFollowPathStatic(void) 0x4F99F0
/*thiscall*/ void CPed::SetFormation(eFormation) 0x51A020
/*thiscall*/ void CPed::SetGetUp(void) 0x4FCF60
/*thiscall*/ void CPed::SetIdle(void) 0x4FDFD0
/*thiscall*/ void CPed::SetInTheAir(void) 0x4FD610
/*thiscall*/ void CPed::SetInvestigateEvent(eEventType eventType,CVector2D,float,ushort,float) 0x527490
/*thiscall*/ void CPed::SetJump(void) 0x4F03C0
/*thiscall*/ void CPed::SetLanding(void) 0x4FD3A0
/*thiscall*/ void CPed::SetLeader(CPed* ped) 0x4F07D0
/*thiscall*/ void CPed::SetLook(CEntity *entity) 0x4FCB10
/*thiscall*/ void CPed::SetLookFlag(CEntity *lookingTo,bool likeUnused,bool) 0x50BB70
/*thiscall*/ void CPed::SetLookFlag(float lookHeading,bool likeUnused,bool) 0x50BC40
/*thiscall*/ void CPed::SetLookTimer(uint time) 0x4FCAF0
/*thiscall*/ void CPed::SetMoveState(eMoveState moveState) 0x50D110
/*thiscall*/ void CPed::SetNewAttraction(CPedAttractor *,CVector const&,float,float,int) 0x4EF7C0
/*thiscall*/ void CPed::SetObjective(eObjective objective) 0x5224B0
/*thiscall*/ void CPed::SetObjective(eObjective objective,CVector) 0x521840
/*thiscall*/ void CPed::SetObjective(eObjective objective,float,CVector const&) 0x5217E0
/*thiscall*/ void CPed::SetObjective(eObjective objective,short,short) 0x521D10
/*thiscall*/ void CPed::SetObjective(eObjective objective,void *) 0x521F10
/*thiscall*/ void CPed::SetObjectiveTimer(uint time) 0x522660
/*thiscall*/ void CPed::SetPedPositionInCar(void) 0x4F42F0
/*thiscall*/ void CPed::SetPedStats(ePedStats statsType) 0x50D8E0
/*thiscall*/ void CPed::SetPointGunAt(CEntity *entity) 0x52DDF0
/*thiscall*/ void CPed::SetRadioStation(void) 0x4EFBD0
/*thiscall*/ void CPed::SetSeek(CEntity *,float) 0x4FC570
/*thiscall*/ void CPed::SetSeek(CVector,float) 0x4FC740
/*thiscall*/ void CPed::SetSeekBoatPosition(CVehicle *boat) 0x512850
/*thiscall*/ void CPed::SetSeekCar(CVehicle *car,uint) 0x4F54D0
/*thiscall*/ void CPed::SetShootTimer(uint time) 0x4FCA90
/*thiscall*/ void CPed::SetSolicit(uint) 0x4F1400
/*thiscall*/ void CPed::SetStoredObjective(void) 0x522620
/*thiscall*/ void CPed::SetStoredState(void) 0x50CC40
/*thiscall*/ void CPed::SetWaitState(eWaitState waitState,void *) 0x4F28A0
/*thiscall*/ void CPed::SetWanderPath(char arg0) 0x4FACC0
/*thiscall*/ void CPed::Solicit(void) 0x4F11D0
/*thiscall*/ void CPed::SortPeds(CPed** pedList,int,int) 0x50D120
/*thiscall*/ void CPed::SpawnFlyingComponent(int,char arg1) 0x5259F0
/*thiscall*/ void CPed::StartFightAttack(uchar) 0x52AD70
/*thiscall*/ void CPed::StartFightDefend(uchar,uchar,uchar) 0x52A340
/*thiscall*/ void CPed::StopNonPartialAnims(void) 0x50CD20
/*thiscall*/ bool CPed::TurnBody(void) 0x4FC970
/*thiscall*/ void CPed::Undress(char const* modelName) 0x4EF030
/*thiscall*/ void CPed::UpdateFromLeader(void) 0x521070
/*thiscall*/ void CPed::UpdatePosition(void) 0x50A040
/*thiscall*/ bool CPed::UseGroundColModel(void) 0x501900
/*thiscall*/ void CPed::Wait(void) 0x4F18A0
/*thiscall*/ void CPed::WanderPath(void) 0x4FA680
/*thiscall*/ void CPed::WarpPedIntoCar(CVehicle *vehicle) 0x4EF8B0
/*thiscall*/ void CPed::WarpPedToNearEntityOffScreen(CEntity *entity) 0x5110C0
/*thiscall*/ void CPed::WarpPedToNearLeaderOffScreen(void) 0x511480
/*thiscall*/ bool CPed::WillChat(CPed* ped) 0x50AC70
/*thiscall*/ float CPed::WorkOutHeadingForMovingFirstPerson(float heading) 0x50A530
/*cdecl*/ void CPed::operator delete(void *data) 0x50DA20
/*cdecl*/ void* CPed::operator new(uint size) 0x50DA60
/*cdecl*/ void* CPed::operator new(uint size,int) 0x50DA40
/*thiscall*/ void CPed::CPed(uint modelIndex) 0x50DC20
/*thiscall*/ void CPedModelInfo::AnimatePedColModelSkinned(RpClump * clump) 0x566150
/*thiscall*/ void CPedModelInfo::AnimatePedColModelSkinnedWorld(RpClump * clump) 0x566060
/*thiscall*/ void CPedModelInfo::CreateHitColModelSkinned(RpClump * clump) 0x566300
/*cdecl*/ bool CPedPlacement::FindZCoorForPed(CVector *posn) 0x52FA60
/*cdecl*/ bool CPedPlacement::IsPositionClearForPed(CVector const& posn, float, int, CEntity **entity) 0x52FBD0
/*cdecl*/ bool CPedPlacement::IsPositionClearOfCars(CVector *posn) 0x52FBA0
CPedStats* CPedStats::ms_apPedStats[40] 0x938828
/*cdecl*/ void CPedStats::Initialise(void) 0x530260
/*cdecl*/ void CPedStats::Shutdown(void) 0x530220
/*cdecl*/ void CPedStats::LoadPedStats(void) 0x530020
/*cdecl*/ uint CPedStats::GetPedStatType(char *pedStatName) 0x52FFC0
CPedType* CPedType::ms_apPedType[23] 0xA0DA64
/*cdecl*/ void CPedType::Initialise(void) 0x530F00
/*cdecl*/ void CPedType::Shutdown(void) 0x530EC0
/*cdecl*/ void CPedType::LoadPedData(void) 0x530B90
/*cdecl*/ uint CPedType::FindPedType(char* pedName) 0x530860
/*cdecl*/ uint CPedType::FindPedFlag(char* flagName) 0x530480
/*cdecl*/ void CPedType::Save(uchar* bufferPointer, uint* structSize) 0x5303D0
/*cdecl*/ void CPedType::Load(uchar* bufferPointer, uint structSize) 0x530340
/*thiscall*/ void CPhone::CPhone(void) 0x43CD40
/*thiscall*/ void CPhone::~CPhone(void) 0x43CD30
void CPhysical::ProcessEntityCollision(CEntity *, CColPoint *) 0x0
/*cdecl*/ void CPhysical::PlacePhysicalRelativeToOtherPhysical(CPhysical* phys1,CPhysical* phys2,CVector offset) 0x4AF100
/*thiscall*/ void CPhysical::RemoveRefsToEntity(CEntity *entity) 0x4AF1D0
/*thiscall*/ bool CPhysical::ProcessCollisionSectorList_SimpleCar(CSector *sector) 0x4AF2E0
/*thiscall*/ bool CPhysical::ProcessShiftSectorList(CPtrList *ptrList) 0x4B02B0
/*thiscall*/ bool CPhysical::ProcessCollisionSectorList(CPtrList *ptrList) 0x4B1070
/*thiscall*/ bool CPhysical::ApplyFriction(CPhysical* phys,float,CColPoint &colPoint) 0x4B39F0
/*thiscall*/ bool CPhysical::ApplyFriction(float,CColPoint &colPoint) 0x4B5200
/*thiscall*/ bool CPhysical::ApplySpringDampening(float,CVector &,CVector &,CVector &) 0x4B5810
/*thiscall*/ bool CPhysical::ApplySpringCollisionAlt(float,CVector &,CVector &,float,float,CVector &) 0x4B5AB0
/*thiscall*/ bool CPhysical::ApplySpringCollision(float,CVector &,CVector &,float,float) 0x4B5C60
/*thiscall*/ bool CPhysical::ApplyCollisionAlt(CEntity *entity,CColPoint &colPoint,float &,CVector &,CVector &) 0x4B5DB0
/*thiscall*/ bool CPhysical::ApplyCollision(CPhysical* phys,CColPoint &colPoint,float &,float &) 0x4B6600
/*thiscall*/ bool CPhysical::ApplyCollision(CColPoint &colPoint,float &) 0x4B8AA0
/*thiscall*/ void CPhysical::ApplyTurnSpeed(void) 0x4B8EC0
/*thiscall*/ bool CPhysical::GetHasCollidedWith(CEntity *entity) 0x4B9010
/*thiscall*/ void CPhysical::AddCollisionRecord(CEntity *entity) 0x4B9050
/*thiscall*/ bool CPhysical::CheckCollision(void) 0x4B9450
/*thiscall*/ void CPhysical::ApplyFrictionTurnForce(float,float,float,float,float,float) 0x4BAA00
/*thiscall*/ void CPhysical::ApplyAirResistance(void) 0x4BAB00
/*thiscall*/ void CPhysical::ApplyMoveSpeed(void) 0x4BAC70
/*thiscall*/ void CPhysical::ApplyTurnForce(float,float,float,float,float,float) 0x4BACC0
/*thiscall*/ void CPhysical::ApplyMoveForce(float x,float y,float z) 0x4BADC0
/*thiscall*/ void CPhysical::RemoveFromMovingList(void) 0x4BAE30
/*thiscall*/ void CPhysical::AddToMovingList(void) 0x4BAE90
/*thiscall*/ void CPhysical::RemoveAndAdd(void) 0x4BAEE0
int CPickups::PlayerOnWeaponPickup 0x978744
int CPickups::StaticCamStartTime 0x974C24
CVector CPickups::StaticCamCoors 0xA0CFA0
CVehicle* CPickups::pPlayerVehicle 0x978D90
Bool CPickups::bPickUpcamActivated 0xA10B20
short CPickups::CollectedPickUpIndex 0xA10A4A
int CPickups::aPickUpsCollected[20] 0x94AF48
short CPickups::NumMessages 0xA10A5A
tPickupMessage CPickups::aMessages[16] 0x7E9B08
CPickup CPickups::aPickUps[336] 0x945D30
/*thiscall*/ int CPickup::GiveUsAPickUpObject(CObject **,CObject **,int,int) 0x43D3B0
/*thiscall*/ void CPickup::Update(CPlayerPed *,CVehicle *vehicle,int) 0x440030
/*thiscall*/ void CPickup::CPickup(void) 0x441F30
/*cdecl*/ void CPickups::CreateSomeMoney(CVector posn,int) 0x43E180
/*cdecl*/ void CPickups::DoCollectableEffects(CEntity *entity) 0x43ED40
/*cdecl*/ void CPickups::DoMineEffects(CEntity *entity) 0x43E840
/*cdecl*/ void CPickups::DoMoneyEffects(CEntity *entity) 0x43EAC0
/*cdecl*/ void CPickups::DoPickUpEffects(CEntity *entity) 0x43F050
/*cdecl*/ int CPickups::GenerateNewOne(CVector posn,uint,uchar ,uint,uint,bool,char *msg) 0x4418C0
/*cdecl*/ int CPickups::GetActualPickupIndex(int handle) 0x43D360
/*cdecl*/ bool CPickups::GivePlayerGoodiesWithPickUpMI(ushort model,int plrIndex) 0x43D910
/*cdecl*/ void CPickups::Init(void) 0x441D30
/*cdecl*/ bool CPickups::IsPickUpPickedUp(int handle) 0x441880
/*cdecl*/ void CPickups::Load(uchar *,uint) 0x43CF40
/*cdecl*/ int CPickups::ModelForWeapon(eWeaponType weaponType) 0x4418B0
/*cdecl*/ void CPickups::PassTime(uint time) 0x43D8C0
/*cdecl*/ void CPickups::RemoveAllPickupsOfACertainWeaponGroupWithNoAmmo(eWeaponType weaponType) 0x43D240
/*cdecl*/ void CPickups::RemovePickUp(int handle) 0x4417D0
/*cdecl*/ void CPickups::RemoveUnnecessaryPickups(CVector const& posn,float radius) 0x43E4C0
/*cdecl*/ void CPickups::RenderPickUpText(void) 0x43E5E0
/*cdecl*/ void CPickups::Save(uchar *,uint *) 0x43D0D0
/*cdecl*/ void CPickups::Update(void) 0x441BB0
/*thiscall*/ void CPlaceable::CPlaceable(void) 0x4BBAD0
/*thiscall*/ bool CPlaceable::IsWithinArea(float x1,float y1,float z1,float x2,float y2,float z2) 0x4BB900
/*thiscall*/ bool CPlaceable::IsWithinArea(float x1,float y1,float x2,float y2) 0x4BB9E0
/*thiscall*/ void CPlaceable::SetHeading(float heading) 0x4BBA80
/*thiscall*/ void CPlane::CPlane(int modelIndex, uchar createdBy) 0x5B2B50
/*cdecl*/ void CPlane::InitPlanes(void) 0x5B21E0
/*cdecl*/ bool CPlane::Load(void) 0x5AFAD0
/*cdecl*/ void CPlane::LoadPath(char const*, int &, float &, bool) 0x5B1FF0
/*cdecl*/ bool CPlane::Save(void) 0x5AFB80
/*cdecl*/ void CPlane::Shutdown(void) 0x5B2160
/*cdecl*/ bool CPlane::TestRocketCollision(CVector *) 0x5AFC90
/*cdecl*/ void CPlane::UpdatePlanes(void) 0x5B19D0
void __thiscall CPlayerInfo::Clear(void) 0x4BE870
void __thiscall CPlayerInfo::Process(void) 0x4BCA90
bool __thiscall CPlayerInfo::IsPlayerInRemoteMode(void) 0x4BCA60
void __thiscall CPlayerInfo::SavePlayerInfo(unsigned char *bufferPointer, unsigned int *structSize) 0x4BC800
void __thiscall CPlayerInfo::LoadPlayerInfo(unsigned char *bufferPointer, unsigned int structSize) 0x4BC5B0
void __thiscall CPlayerInfo::FindClosestCarSectorList(CPtrList &ptrList, CPed *ped, float conrerAX, float cornerAY, float cornerBX, float cornerBY, float
CVector __thiscall CPlayerInfo::GetPos(void) 0x4BC2A0
bool __thiscall CPlayerInfo::IsRestartingAfterDeath(void) 0x4BBF50
bool __thiscall CPlayerInfo::IsRestartingAfterArrest(void) 0x4BBF30
void __thiscall CPlayerInfo::KillPlayer(void) 0x4BBEE0
void __thiscall CPlayerInfo::ArrestPlayer(void) 0x4BBE90
void __thiscall CPlayerInfo::CancelPlayerEnteringCars(CVehicle *vehicle) 0x4BBE40
void __thiscall CPlayerInfo::MakePlayerSafe(bool safe) 0x4BBC10
void __thiscall CPlayerInfo::BlowUpRCBuggy(bool blowUp) 0x4BBBC0
void __thiscall CPlayerInfo::SetPlayerSkin(char const *skinName) 0x4BBB70
void __thiscall CPlayerInfo::LoadPlayerSkin(void) 0x4BBB30
void __thiscall CPlayerInfo::DeletePlayerSkin(void) 0x4BBB10
/*thiscall*/ void CPlayerPed::AnnoyPlayerPed(bool) 0x531CF0
/*thiscall*/ void CPlayerPed::CPlayerPed(void) 0x5384B0
/*thiscall*/ void CPlayerPed::ClearAdrenaline(void) 0x531CC0
/*thiscall*/ void CPlayerPed::ClearWeaponTarget(void) 0x533B30
/*cdecl*/ void CPlayerPed::DeactivatePlayerPed(int playerId) 0x5383C0
/*thiscall*/ void CPlayerPed::DoStuffToGoOnFire(void) 0x531D20
/*thiscall*/ float CPlayerPed::DoWeaponSmoothSpray(void) 0x536410
/*thiscall*/ bool CPlayerPed::DoesPlayerWantNewWeapon(eWeaponType weaponType,bool enable) 0x535240
/*thiscall*/ void CPlayerPed::EvaluateNeighbouringTarget(CEntity *target,CEntity **outTarget,float *outTargetPriority,float maxDistance,float,bool,bool,bool)
/*thiscall*/ void CPlayerPed::EvaluateTarget(CEntity *target,CEntity **outTarget,float *outTargetPriority,float maxDistance,float,bool,bool) 0x532360
/*thiscall*/ int CPlayerPed::FindMeleeAttackPoint(CPed *,CVector &,uint &) 0x531390
/*thiscall*/ __int16 CPlayerPed::FindNewAttackPoints(void) 0x531810
/*thiscall*/ bool CPlayerPed::FindNextWeaponLockOnTarget(CEntity *target,bool) 0x532590
/*thiscall*/ bool CPlayerPed::FindWeaponLockOnTarget(void) 0x533030
/*thiscall*/ CPlayerInfo* CPlayerPed::GetPlayerInfoForThisPlayerPed(void) 0x531D40
/*thiscall*/ void CPlayerPed::KeepAreaAroundPlayerClear(void) 0x531D60
/*thiscall*/ void CPlayerPed::MakeChangesForNewWeapon(eWeaponType weaponType) 0x534450
/*thiscall*/ void CPlayerPed::MakeChangesForNewWeapon(int weaponSlot) 0x534580
/*thiscall*/ void CPlayerPed::MakeObjectTargettable(int,bool) 0x531FD0
/*thiscall*/ void CPlayerPed::PlayIdleAnimations(CPad *pad) 0x535D10
/*thiscall*/ void CPlayerPed::PlayerControl1stPersonRunAround(CPad *pad) 0x5357D0
/*thiscall*/ void CPlayerPed::PlayerControlFighter(CPad *pad) 0x535BB0
/*thiscall*/ void CPlayerPed::PlayerControlM16(CPad *pad) 0x5352B0
/*thiscall*/ void CPlayerPed::PlayerControlSniper(CPad *pad) 0x535550
/*thiscall*/ void CPlayerPed::PlayerControlZelda(CPad *pad) 0x535F40
/*thiscall*/ void CPlayerPed::ProcessAnimGroups(void) 0x533B80
/*thiscall*/ void CPlayerPed::ProcessPlayerWeapon(CPad *pad) 0x534890
/*thiscall*/ void CPlayerPed::ProcessWeaponSwitch(CPad *pad) 0x5345A0
/*thiscall*/ void CPlayerPed::ReApplyMoveAnims(void) 0x5371B0
/*cdecl*/ void CPlayerPed::ReactivatePlayerPed(int playerId) 0x5383A0
/*thiscall*/ void CPlayerPed::RemovePedFromMeleeList(CPed *ped) 0x5312A0
/*thiscall*/ void CPlayerPed::SetInitialState(void) 0x5381F0
/*thiscall*/ void CPlayerPed::SetNearbyPedsToInteractWithPlayer(void) 0x530FB0
/*thiscall*/ void CPlayerPed::SetRealMoveAnim(void) 0x536620
/*thiscall*/ void CPlayerPed::SetWantedLevel(int level) 0x532090
/*thiscall*/ void CPlayerPed::SetWantedLevelNoDrop(int level) 0x532070
/*cdecl*/ void CPlayerPed::SetupPlayerPed(int playerId) 0x5383E0
/*thiscall*/ void CPlayerPed::UpdateMeleeAttackers(void) 0x531600
/*thiscall*/ int CPlayerPed::GetWantedLevel(void) 0x599B20
/*cdecl*/ void CPlayerSkin::BeginFrontendSkinEdit(void) 0x627D10
/*cdecl*/ void CPlayerSkin::EndFrontendSkinEdit(void) 0x627CE0
/*cdecl*/ int CPlayerSkin::GetSkinTexture(char const*) 0x627E60
/*cdecl*/ void CPlayerSkin::Initialise(void) 0x627FB0
/*cdecl*/ void CPlayerSkin::RenderFrontendSkinEdit(void) 0x627BC0
/*cdecl*/ void CPlayerSkin::Shutdown(void) 0x627FA0
/*cdecl*/ void CPools::MakeSureSlotInObjectPoolIsEmpty(int slot) 0x4BEA80
/*cdecl*/ void CPools::LoadPedPool(uchar *buffer,uint size) 0x4BEB50
/*cdecl*/ void CPools::SavePedPool(uchar *buffer,uint *outSize) 0x4BEDC0
/*cdecl*/ void CPools::LoadObjectPool(uchar *buffer,uint size) 0x4BEF70
/*cdecl*/ void CPools::SaveObjectPool(uchar *buffer,uint *outSize) 0x4BF420
/*cdecl*/ void CPools::SaveVehiclePool(uchar *buffer,uint *outSize) 0x4BF6D0
/*cdecl*/ void CPools::LoadVehiclePool(uchar *buffer,uint size) 0x4BF9A0
/*cdecl*/ CObject* CPools::GetObject(int handle) 0x4BFF80
/*cdecl*/ int CPools::GetObjectRef(CObject *object) 0x4BFFA0
/*cdecl*/ CVehicle* CPools::GetVehicle(int handle) 0x4BFFC0
/*cdecl*/ int CPools::GetVehicleRef(CVehicle *vehicle) 0x4BFFE0
/*cdecl*/ CPed* CPools::GetPed(int handle) 0x4C0000
/*cdecl*/ int CPools::GetPedRef(CPed *ped) 0x4C0020
/*cdecl*/ void CPools::CheckPoolsEmpty(void) 0x4C0040
/*cdecl*/ void CPools::ShutDown(void) 0x4C0070
/*cdecl*/ void CPools::Initialise(void) 0x4C0270
/*cdecl*/ CPed* CPopulation::AddDeadPedInFrontOfCar(CVector const& posn,CVehicle * vehicle) 0x53B180
/*cdecl*/ CPed* CPopulation::AddPed(ePedType pedType,uint modelIndex,CVector const& posn,int) 0x53B600
/*cdecl*/ CPed* CPopulation::AddPedInCar(CVehicle * vehicle,bool driver) 0x53A8A0
/*cdecl*/ void CPopulation::AddToPopulation(float,float,float,float) 0x53BA80
/*cdecl*/ bool CPopulation::CanJeerAtStripper(int modelIndex) 0x53A670
/*cdecl*/ bool CPopulation::CanSolicitPlayerInCar(int modelIndex) 0x53A6A0
/*cdecl*/ bool CPopulation::CanSolicitPlayerOnFoot(int modelIndex) 0x53A6C0
/*cdecl*/ void CPopulation::ChooseCivilianCoupleOccupations(int,int &,int &) 0x53AE90
/*cdecl*/ int CPopulation::ChooseCivilianOccupation(int) 0x53B070
/*cdecl*/ int CPopulation::ChooseNextCivilianOccupation(int) 0x53AFD0
/*cdecl*/ void CPopulation::ConvertAllObjectsToDummyObjects(void) 0x53D430
/*cdecl*/ void CPopulation::ConvertToDummyObject(CObject * object) 0x53D290
/*cdecl*/ void CPopulation::ConvertToRealObject(CDummyObject * dummyObject) 0x53D340
/*cdecl*/ void CPopulation::GeneratePedsAtStartOfGame(void) 0x53E3E0
/*cdecl*/ void CPopulation::Initialise(void) 0x53EAF0
/*cdecl*/ bool CPopulation::IsFemale(int modelIndex) 0x53AD50
/*cdecl*/ bool CPopulation::IsMale(int modelIndex) 0x53ADF0
/*cdecl*/ bool CPopulation::IsSkateable(CVector const& point) 0x53ACA0
/*cdecl*/ bool CPopulation::IsSunbather(int modelIndex) 0x53A6F0
/*cdecl*/ void CPopulation::LoadPedGroups(void) 0x53E9C0
/*cdecl*/ void CPopulation::ManagePopulation(void) 0x53D690
/*cdecl*/ void CPopulation::PlaceCouple(ePedType pedType1,int modelIndex1,ePedType pedType2,int modelIndex2,CVector posn) 0x5388F0
/*cdecl*/ void CPopulation::PlaceGangMembersInCircle(ePedType pedType,int modelIndex,CVector const& posn) 0x5397F0
/*cdecl*/ void CPopulation::PlaceGangMembersInFormation(ePedType pedType,int modelIndex,CVector const& posn) 0x539FC0
/*cdecl*/ void CPopulation::PlaceMallPedsAsStationaryGroup(CVector const& posn,int modelIndex) 0x538E90
/*cdecl*/ void CPopulation::RemovePed(CPed * ped) 0x53B160
/*cdecl*/ void CPopulation::RemovePedsIfThePoolGetsFull(void) 0x53D560
/*cdecl*/ bool CPopulation::TestSafeForRealObject(CDummyObject * dummyObject) 0x53CF80
/*cdecl*/ void CPopulation::Update(bool generatePeds) 0x53E5F0
/*cdecl*/ void CPopulation::UpdatePedCount(ePedType pedType,uchar updateState) 0x53A720
/*thiscall*/ void CProjectile::CProjectile(int) 0x4E8D30
/*cdecl*/ void CPtrNode::operator delete(void *data) 0x4C1500
/*cdecl*/ void* CPtrNode::operator new(uint size) 0x4C1520
/*thiscall*/ void CPtrList::Flush(void) 0x4C14B0
/*thiscall*/ void CQuaternion::Get(RwMatrixTag *) 0x4DFD30
/*thiscall*/ void CQuaternion::Set(RwV3d *axis, float angle) 0x4DFE20
/*thiscall*/ void CQuaternion::Slerp(CQuaternion const& from,CQuaternion const& to, float halftheta, float sintheta_inv, float t) 0x4DFBE0
/*thiscall*/ void CRGBA::CRGBA(uchar r, uchar g, uchar b, uchar a) 0x541570
/*thiscall*/ void CRunningScript::Init(void) 0x450CF0
/*thiscall*/ char CRunningScript::ProcessOneCommand(void) 0x44FBE0
void CSimpleModelInfo::SetAtomic(int atomicIndex, RpAtomic *atomic) 0x56F790
/*thiscall*/ RpAtomic* CSimpleModelInfo::GetAtomicFromDistance(float distance) 0x56F690
/*thiscall*/ float CSimpleModelInfo::GetLargestLodDistance(void) 0x56F660
/*thiscall*/ RpAtomic* CSimpleModelInfo::GetLastAtomic(float distance) 0x56F620
/*thiscall*/ float CSimpleModelInfo::GetLodDistance(int lodIndex) 0x56F6F0
/*thiscall*/ void CSimpleModelInfo::Init(void) 0x56F770
/*thiscall*/ void CSimpleModelInfo::SetLodDistances(float *distances) 0x56F600
/*thiscall*/ void CSimpleModelInfo::SetupBigBuilding(int minLineIndex,int maxLineIndex) 0x56F420
/*cdecl*/ void CSprite2d::DrawAnyRect(float x1,float y1,float x2,float y2,float x3,float y3,float x4,float y4,CRGBA const& color1,CRGBA const& color2,CRGBA
/*cdecl*/ void CSprite2d::DrawRect(CRect const&rect,CRGBA const&color1,CRGBA const&color2,CRGBA const&color3,CRGBA const&color4) 0x577A80
/*cdecl*/ void CSprite2d::DrawRect(CRect const&rect,CRGBA const&color) 0x577B00
/*thiscall*/ void CSprite2d::SetRenderState(void) 0x577B90
/*cdecl*/ void CSprite2d::SetVertices(RwIm2DVertex *vertices,CRect const&rect,CRGBA const&color1,CRGBA const&color2,CRGBA const&color3,CRGBA const&color4,float
/*cdecl*/ void CSprite2d::SetMaskVertices(int numVerts,float *posn) 0x577D10
/*cdecl*/ void CSprite2d::SetVertices(int numVerts,float *posn,float *texCoors,CRGBA const&color) 0x577F70
/*cdecl*/ void CSprite2d::SetVertices(CRect const&,CRGBA const&,CRGBA const&,CRGBA const&,CRGBA const&,float,float,float,float,float,float,float,float) 0x578010
/*cdecl*/ void CSprite2d::SetVertices(float x1,float y1,float x2,float y2,float x3,float y3,float x4,float y4,CRGBA const&color1,CRGBA const&color2,CRGBA
/*cdecl*/ void CSprite2d::SetVertices(CRect const&rect,CRGBA const&color1,CRGBA const&color2,CRGBA const&color3,CRGBA const&color4) 0x578370
/*cdecl*/ void CSprite2d::Draw2DPolygon(float x1,float y1,float x2,float y2,float x3,float y3,float x4,float y4,CRGBA const&color) 0x578520
/*thiscall*/ void CSprite2d::Draw(float x1,float y1,float x2,float y2,float x3,float y3,float x4,float y4,CRGBA const&color) 0x5785D0
/*thiscall*/ void CSprite2d::Draw(CRect const&rect,CRGBA const&color1,CRGBA const&color2,CRGBA const&color3,CRGBA const&color4) 0x578640
/*thiscall*/ void CSprite2d::Draw(CRect const&rect,CRGBA const&color,float u1,float v1,float u2,float v2,float u3,float v3,float u4,float v4) 0x5786A0
/*thiscall*/ void CSprite2d::Draw(CRect const&rect,CRGBA const&color) 0x578710
/*thiscall*/ void CSprite2d::DrawRectXLU(CRect const&rect,CRGBA const&color1,CRGBA const&color2,CRGBA const&color3,CRGBA const&color4) 0x578760
/*cdecl*/ void CSprite2d::RenderVertexBuffer(void) 0x5787E0
/*cdecl*/ void CSprite2d::AddToBuffer(CRect const&rect,CRGBA const&color,float u1,float v1,float u2,float v2,float u3,float v3,float u4,float v4) 0x578830
/*cdecl*/ void CSprite2d::InitPerFrame(void) 0x578930
/*thiscall*/ void CSprite2d::SetAddressing(RwTextureAddressMode addressing) 0x578970
/*thiscall*/ void CSprite2d::SetTexture(char *name,char *maskName) 0x5789B0
/*thiscall*/ void CSprite2d::SetTexture(char *name) 0x5789E0
/*cdecl*/ void CSprite2d::SetRecipNearClip(void) 0x578A10
/*thiscall*/ void CSprite2d::Delete(void) 0x578A20
/*thiscall*/ void CSprite2d::~CSprite2d() 0x578A40
/*thiscall*/ void CSprite2d::CSprite2d(void) 0x578A60
float CStats::FavoriteRadioStationList[10] 0x862460
Bool CStats::abSonyCDs[1] 0xA10B88
Bool32 CStats::ShowChaseStatOnScreen 0x97F2C4
Bool32 CStats::NoMoreHurricanes 0xA0FCAC
Bool32 CStats::PamphletMissionPassed 0x97F348
Bool32 CStats::SuburbanPassed 0x978A0C
Bool32 CStats::CommercialPassed 0x9B489C
Bool32 CStats::IndustrialPassed 0x9751F4
char CStats::LastMissionPassedName[8] 0x7E9D78
int CStats::TotalLegitimateKills 0x9B6AB0
int CStats::KillsSinceLastCheckpoint 0x97F2E8
int CStats::CheatedCount 0x9B5F8C
float CStats::HighestChaseValue 0x978E0C
int CStats::BestPositions[1] 0xA0FD80
int CStats::HighestScores[5] 0x9B6E20
int CStats::FastestTimes[23] 0x974B80
int CStats::PropertyDestroyed 0x975404
float CStats::AutoPaintingBudget 0xA10298
float CStats::PropertyBudget 0x9B48B0
float CStats::Longest2WheelDist 0x9B48D0
float CStats::LongestStoppieDist 0x9B5F44
float CStats::LongestWheelieDist  0x9786C0
int CStats::Longest2Wheel 0xA0FCF8
int CStats::LongestStoppie 0x974B3C
int CStats::LongestWheelie 0x97530C
Bool CStats::PropertyOwned[15] 0xA10AFD
int CStats::BloodRingTime 0xA0D2E0
int CStats::BloodRingKills 0x9B6E54
int CStats::NumPropertyOwned 0x978E08
float CStats::ShootingRank 0x974B08
float CStats::TopShootingRangeScore 0xA0D8A4
float CStats::IceCreamSold 0x975390
float CStats::GarbagePickups 0x974C00
float CStats::PizzasDelivered 0x978780
float CStats::Assassinations 0xA10918
float CStats::MovieStunts 0xA0FC8C
float CStats::StoresKnockedOff 0x97F898
float CStats::LoanSharks 0x974C28
float CStats::FashionBudget 0xA0D068
float CStats::WeaponBudget 0xA0FDCC
int CStats::SeagullsKilled 0x97869C
int CStats::TimesDrowned 0x9B48B4
int CStats::FlightTime 0x97854C
int CStats::TotalNumberMissions 0x974BF0
int CStats::TotalNumberKillFrenzies 0x974C0C
int CStats::NumberKillFrenziesPassed 0x974C08
int CStats::PhotosTaken 0x97F21C
int CStats::HighestLevelFireMission 0x975310
int CStats::HighestLevelAmbulanceMission 0x978DB8
int CStats::HighestLevelVigilanteMission 0x94DD60
int CStats::FiresExtinguished 0x9B6A84
int CStats::CriminalsCaught 0x9787B4
int CStats::LivesSavedWithAmbulance 0x9B5EA8
float CStats::DistanceTravelledByPlane 0x9B6A78
float CStats::DistanceTravelledByHelicoptor 0x9B6A48
float CStats::DistanceTravelledByGolfCart 0x974C04
float CStats::DistanceTravelledByBoat 0xA0D384
float CStats::DistanceTravelledByBike 0xA0D2D8
float CStats::DistanceTravelledByCar 0xA0FCFC
float CStats::DistanceTravelledOnFoot 0xA0D9B4
int CStats::MoneyMadeWithTaxi 0xA0D9C8
int CStats::PassengersDroppedOffWithTaxi 0xA0D1DC
int CStats::MissionsPassed 0xA0D224
int CStats::MissionsGiven 0xA1023C
int CStats::TotalNumberOfUniqueJumps 0x978530
int CStats::NumberOfUniqueJumpsFound 0x974B48
int CStats::BestStuntJump 0x974B30
int CStats::MaximumJumpSpins 0x978D14
int CStats::MaximumJumpFlips 0x9787DC
float CStats::MaximumJumpHeight 0xA0CFD8
float CStats::MaximumJumpDistance 0x97F210
int CStats::Sprayings 0xA0FC94
int CStats::SafeHouseVisits 0xA0D228
int CStats::DaysPassed 0x97F1F4
int CStats::TimesDied 0x975320
int CStats::TimesArrested 0x975330
int CStats::WantedStarsEvaded 0x9B5F30
int CStats::WantedStarsAttained 0x9B5EB8
int CStats::HeadsPopped 0x9B6E38
int CStats::BulletsThatHit 0x9B6CD4
int CStats::KgsOfExplosivesUsed 0x9787A8
float CStats::TotalProgressInGame 0x974B0C
float CStats::ProgressMade 0x9B6CDC
int CStats::HelisDestroyed  0x9751F0
int CStats::PedsKilledOfThisType[23] 0x94DB64
int CStats::RoundsFiredByPlayer 0x97532C
int CStats::TyresPopped 0x94DB58
int CStats::BoatsExploded 0x974B04
int CStats::CarsExploded 0xA0D388
int CStats::PeopleKilledByOthers 0x9753AC
int CStats::PeopleKilledByPlayer 0x978794
static void __cdecl CStats::RegisterFastestTime(int statID,int time) 0x4CE3D1
static void __cdecl CStats::RegisterHighestScore(int statID,int score) 0x4CE3B4
static void __cdecl CStats::RegisterBestPosition(int statID,int position) 0x4CE397
static void __cdecl CStats::Init() 0x4CE3FB
static float __cdecl CStats::GetFavoriteRadioStationList(int stationID) 0x4CE38B
static void __cdecl CStats::AnotherLifeSavedWithAmbulance() 0x4CE384
static void __cdecl CStats::AnotherCriminalCaught() 0x4CE37D
static void __cdecl CStats::AnotherFireExtinguished() 0x4CE376
static void __cdecl CStats::RegisterLevelVigilanteMission(int level) 0x4CE35F
static void __cdecl CStats::RegisterLevelAmbulanceMission(int level) 0x4CE348
static void __cdecl CStats::RegisterLevelFireMission(int level) 0x4CE331
static char const* __cdecl CStats::FindChaseString(float chaseValue) 0x4CDBAE
static void __cdecl CStats::AnotherKillFrenzyPassed() 0x4CDBA7
static void __cdecl CStats::SetTotalNumberKillFrenzies(int number) 0x4CDB9D
static void __cdecl CStats::SetTotalNumberMissions(int number) 0x4CDB93
static void __cdecl CStats::MoneySpentOnWeapons(int moneySpent) 0x4CDB82
static void __cdecl CStats::MoneySpentOnProperty(int moneySpent) 0x4CDB71
static void __cdecl CStats::MoneySpentOnFashion(int moneySpent) 0x4CDB60
static void __cdecl CStats::NumOfStoresKnockedOff(int storesKnockedOff) 0x4CDB4F
static void __cdecl CStats::NumOfAssassinations(int assassinations) 0x4CDB3E
static void __cdecl CStats::NumOfPizzasDelivered(int pizzasDelivered) 0x4CDB2D
static void __cdecl CStats::NumOfIceCreamSold(int iceCreamSold) 0x4CDB1C
static void __cdecl CStats::AddPropertyAsOwned(int propertyID) 0x4CDB01
static void __cdecl CStats::AddNumBloodRingKills(int bloodringKills) 0x4CDAF6
static void __cdecl CStats::LongestTimeInBloodRing(int bloodRingTime) 0x4CDAE4
static void __cdecl CStats::CheckPointReachedSuccessfully() 0x4CDAD1
static void __cdecl CStats::CheckPointReachedUnsuccessfully() 0x4CDAC9
static int __cdecl CStats::FindCriminalRatingNumber() 0x4CD97B
static char const* __cdecl CStats::FindCriminalRatingString() 0x4CDDC5
static float __cdecl CStats::GetPercentageProgress() 0x4CD907
static void __cdecl CStats::BuildStatLine(char *a1,void *a2,int a3,void *a4,int a5) 0x4CAE8F
static void __cdecl CStats::SaveStats(unsigned char * bufferPointer,unsigned int *structSize) 0x4CA9F7
static void __cdecl CStats::LoadStats(unsigned char * bufferPointer,unsigned int structSize) 0x4CA5BB
static void __cdecl CStats::ConstructStatLine(int a1) 0x4CB085
/*cdecl*/ void CTheZones::CreateZone(char *name,eZoneType type,float posX1,float posY1,float posZ1,float posX2,float posY2, float posZ2,eLevelName island)
/*cdecl*/ CZone* CTheZones::FindAudioZone(CVector *point) 0x4DC370
/*cdecl*/ int CTheZones::FindInformationZoneForPosition(CVector const* pPoint) 0x4DD160
/*cdecl*/ short CTheZones::FindNextZoneByLabelAndReturnIndex(char *name,eZoneType type) 0x4DD4A0
/*cdecl*/ int CTheZones::FindSmallestNavigationZoneForPosition(CVector const* pPoint,bool,bool) 0x4DD060
/*cdecl*/ short CTheZones::FindZoneByLabelAndReturnIndex(char *name,eZoneType type) 0x4DD5F0
/*cdecl*/ eLevelName CTheZones::GetLevelFromPosition(CVector const* pPoint) 0x4DD300
/*cdecl*/ int CTheZones::GetNavigationZone(ushort) 0x4DCC20
/*cdecl*/ CZone* CTheZones::GetZoneInfo(CVector const* pPoint,uchar) 0x4DCEA0
/*cdecl*/ __int16 CTheZones::GetZoneInfoForTimeOfDay(CVector const* pPoint,CZoneInfo *zoneInfo) 0x4DC500
/*cdecl*/ void CTheZones::Init(void) 0x4DDFA0
/*cdecl*/ void CTheZones::InitialiseAudioZoneArray(void) 0x4DC430
/*cdecl*/ bool CTheZones::InsertZoneIntoZoneHierRecursive(CZone *currentZona, CZone *otherZone) 0x4DD9D0
/*cdecl*/ void CTheZones::LoadAllZones(uchar *,uint) 0x4DBCB0
/*cdecl*/ void CTheZones::LoadOneZone(CZone *pZone,uchar **,uint *,eZoneType type) 0x4DBB80
/*cdecl*/ bool CTheZones::PointLiesWithinZone(CVector const* pPoint,CZone *pZone) 0x4DD750
/*cdecl*/ char CTheZones::PostZoneCreation(void) 0x4DDA90
/*cdecl*/ void CTheZones::SaveAllZones(uchar *,uint *) 0x4DC090
/*cdecl*/ void CTheZones::SaveOneZone(CZone *pZone,uchar **,uint *,eZoneType type) 0x4DBF30
/*cdecl*/ void CTheZones::SetPedGroup(ushort,uchar,ushort) 0x4DCC30
/*cdecl*/ void CTheZones::SetZoneCarInfo(int,uchar,short,short,short const*) 0x4DCDF0
/*cdecl*/ void CTheZones::SetZoneCivilianCarInfo(int,uchar,short const*,short const*) 0x4DCD40
/*cdecl*/ void CTheZones::SetZonePedInfo(int,uchar,short,short,short,short,short,short,short,short,short,short,short) 0x4DCC70
/*cdecl*/ void CTheZones::Update(void) 0x4DDDF0
/*cdecl*/ bool CTheZones::ZoneIsEntirelyContainedWithinOtherZone(CZone *currentZona,CZone *otherZone) 0x4DD7D0
/*thiscall*/ void CTimeModelInfo::FindOtherTimeModel(void) 0x56F330
/*cdecl*/ void CTimer::EndUserPause(void) 0x4D0D90
/*cdecl*/ void CTimer::StartUserPause(void) 0x4D0DA0
/*cdecl*/ void CTimer::Stop(void) 0x4D0DB0
/*cdecl*/ bool CTimer::GetIsSlowMotionActive(void) 0x4D0DC0
/*cdecl*/ uint CTimer::GetCurrentTimeInCycles(void) 0x4D0DF0
/*cdecl*/ uint CTimer::GetCyclesPerMillisecond(void) 0x4D0E30
/*cdecl*/ void CTimer::Resume(void) 0x4D0E50
/*cdecl*/ void CTimer::Suspend(void) 0x4D0ED0
/*cdecl*/ void CTimer::Update(void) 0x4D0F30
/*cdecl*/ void CTimer::Shutdown(void) 0x4D12F0
/*cdecl*/ void CTimer::Initialise(void) 0x4D1300
/*thiscall*/ void CTrain::AddPassenger(CPed * ped) 0x5B2C60
/*thiscall*/ void CTrain::CTrain(int modelIndex, uchar createdBy) 0x5B2D00
/*cdecl*/ void CTrain::InitTrains(void) 0x5B2CA0
/*cdecl*/ void CTrain::Shutdown(void) 0x5B2C90
/*cdecl*/ void CTrain::UpdateTrains(void) 0x5B2C80
/*thiscall*/ float cTransmission::CalculateDriveAcceleration(float const& gasPedal,uchar & currrentGear,float &,float const&,bool) 0x5B2E20
/*thiscall*/ void cTransmission::CalculateGearForSimpleCar(float velocity,uchar & currrentGear) 0x5B2DC0
/*thiscall*/ void cTransmission::InitGearRatios(void) 0x5B3120
/*thiscall*/ void cTransmission::cTransmission(void) 0x5B3240
/*cdecl*/ void* CTreadable::operator new(uint size) 0x407FF0
/*thiscall*/ void CTreadable::CTreadable(void) 0x408020
/*cdecl*/ TxdDef* CTxdStore::AddRef(int index) 0x580A60
/*cdecl*/ int CTxdStore::AddTxdSlot(char const* name) 0x580F00
/*cdecl*/ void CTxdStore::Create(int index) 0x580B60
/*cdecl*/ int CTxdStore::FindTxdSlot(char const* name) 0x580D70
/*cdecl*/ bool CTxdStore::FinishLoadTxd(int index,RwStream *stream) 0x580BA0
/*cdecl*/ void CTxdStore::GameShutdown(void) 0x580F40
/*cdecl*/ int CTxdStore::GetNumRefs(int index) 0x580990
/*cdecl*/ int CTxdStore::GetTxdName(int index) 0x580E50
/*cdecl*/ bool CTxdStore::LoadTxd(int index, RwStream *stream) 0x580C60
/*cdecl*/ bool CTxdStore::LoadTxd(int index, char const* filename) 0x580CD0
/*cdecl*/ void CTxdStore::PopCurrentTxd(void) 0x580AA0
/*cdecl*/ void CTxdStore::PushCurrentTxd(void) 0x580AC0
/*cdecl*/ void CTxdStore::RemoveRef(int index) 0x580A10
/*cdecl*/ TxdDef* CTxdStore::RemoveRefWithoutDelete(int index) 0x5809D0
/*cdecl*/ void CTxdStore::RemoveTxd(int index) 0x580B10
/*cdecl*/ void CTxdStore::RemoveTxdSlot(int index) 0x580E90
/*cdecl*/ void CTxdStore::SetCurrentTxd(int index) 0x580AD0
/*cdecl*/ void CTxdStore::Shutdown(void) 0x580FF0
/*cdecl*/ bool CTxdStore::StartLoadTxd(int index,RwStream *stream) 0x580BF0
/*cdecl*/ void CTxdStore::Initialise(void) 0x581010
/*cdecl*/ void CUserDisplay::Init(void) 0x4D1490
/*cdecl*/ void CUserDisplay::Process(void) 0x4D1400
void CVehicle::ProcessControlInputs(uchar playerNum) 0x69CA3C
void CVehicle::GetComponentWorldPosition(int componentId, CVector &posnOut) 0x69CA40
bool CVehicle::IsComponentPresent(int componentId) 0x69CA44
void CVehicle::SetComponentRotation(int componentId, CVector) 0x69CA48
void CVehicle::OpenDoor(int componentId, eDoors door, float doorOpenRatio) 0x69CA4C
void CVehicle::ProcessOpenDoor(uint, uint, float) 0x69CA50
bool CVehicle::IsDoorReady(eDoors door) 0x69CA54
bool CVehicle::IsDoorFullyOpen(eDoors door) 0x69CA58
bool CVehicle::IsDoorClosed(eDoors door) 0x69CA5C
bool CVehicle::IsDoorMissing(eDoors door) 0x69CA60
bool CVehicle::IsDoorReady(uint door) 0x69CA64
bool CVehicle::IsDoorMissing(uint door) 0x69CA68
bool CVehicle::IsOpenTopCar(void) 0x69CA6C
void CVehicle::RemoveRefsToVehicle(CEntity *entity) 0x69CA70
void CVehicle::BlowUpCar(CEntity *damager) 0x69CA74
bool CVehicle::SetUpWheelColModel(CColModel *wheelCol) 0x69CA78
bool CVehicle::BurstTyre(uchar tyreComponentId, bool bPhysicalEffect) 0x69CA7C
bool CVehicle::IsRoomForPedToLeaveCar(uint, CVector *) 0x69CA80
bool CVehicle::IsClearToDriveAway(void) 0x69CA84
float CVehicle::GetHeightAboveRoad(void) 0x69CA88
void CVehicle::PlayCarHorn(void) 0x69CA8C
/*thiscall*/ void CVehicle::ActivateBomb(void) 0x5B79E0
/*thiscall*/ void CVehicle::ActivateBombWhenEntered(void) 0x5B7950
/*thiscall*/ bool CVehicle::AddPassenger(CPed *passenger) 0x5B8E60
/*thiscall*/ bool CVehicle::AddPassenger(CPed *passenger, uchar seatNumber) 0x5B8D50
/*thiscall*/ void CVehicle::BladeColSectorList(CPtrList &ptrList, CColModel &colModel, CMatrix &matrix, short, float) 0x5B4610
/*thiscall*/ bool CVehicle::CanBeDeleted(void) 0x5BA960
/*thiscall*/ bool CVehicle::CanDoorsBeDamaged(void) 0x5B8440
/*thiscall*/ bool CVehicle::CanPedEnterCar(void) 0x5B8370
/*thiscall*/ bool CVehicle::CanPedExitCar(bool) 0x5B8180
/*thiscall*/ bool CVehicle::CanPedJumpOffBike(void) 0x5B8130
/*thiscall*/ bool CVehicle::CanPedJumpOutCar(void) 0x5B80C0
/*thiscall*/ bool CVehicle::CanPedOpenLocks(CPed *ped) 0x5B8460
/*thiscall*/ bool CVehicle::CarHasRoof(void) 0x5B7910
/*thiscall*/ void CVehicle::ChangeLawEnforcerState(uchar state) 0x5B7D90
/*thiscall*/ void CVehicle::DoBladeCollision(CVector, CMatrix &matrix, short, float, float) 0x5B5030
/*thiscall*/ void CVehicle::DoFixedMachineGuns(void) 0x5C9170
/*thiscall*/ void CVehicle::DoSunGlare(void) 0x5B3CD0
/*thiscall*/ void CVehicle::ExtinguishCarFire(void) 0x5B7A80
/*thiscall*/ int CVehicle::FindTyreNearestPoint(float x, float y) 0x5B96A0
/*thiscall*/ void CVehicle::FireFixedMachineGuns(void) 0x5C8E40
/*thiscall*/ void CVehicle::FlyingControl(eFlightModel flightModel) 0x5B54C0
/*thiscall*/ int CVehicle::GetVehicleAppearance(void) 0x5BAA80
/*cdecl*/ void CVehicle::HeliDustGenerate(CEntity *, float, float, int) 0x5B3250
/*thiscall*/ void CVehicle::InflictDamage(CEntity *damager, eWeaponType weapon, float intensity, CVector coords) 0x5B9020
/*thiscall*/ bool CVehicle::IsDriver(CPed *ped) 0x5B8670
/*thiscall*/ bool CVehicle::IsDriver(int modelIndex) 0x5B8640
/*thiscall*/ bool CVehicle::IsLawEnforcementVehicle(void) 0x5B7D60
/*thiscall*/ bool CVehicle::IsOnItsSide(void) 0x5B84B0
/*thiscall*/ bool CVehicle::IsPassenger(CPed *ped) 0x5B86D0
/*thiscall*/ bool CVehicle::IsPassenger(int modelIndex) 0x5B86A0
/*thiscall*/ bool CVehicle::IsSphereTouchingVehicle(float x, float y, float z, float radius) 0x5B7F00
/*thiscall*/ bool CVehicle::IsUpsideDown(void) 0x5B84F0
/*thiscall*/ bool CVehicle::IsVehicleNormal(void) 0x5B7DF0
/*thiscall*/ void CVehicle::KillPedsInVehicle(void) 0x5B8560
/*thiscall*/ void CVehicle::MakeNonDraggedPedsLeaveVehicle(CPed *, CPed *, CPlayerPed *&, CCopPed *&) 0x5B3A30
/*thiscall*/ void CVehicle::ProcessBikeWheel(CVector &, CVector &, CVector &, CVector &, int, float, float, float, float, char, float *, tWheelState *,
/*thiscall*/ void CVehicle::ProcessCarAlarm(void) 0x5B8040
/*thiscall*/ void CVehicle::ProcessDelayedExplosion(void) 0x5B8F50
/*thiscall*/ void CVehicle::ProcessWheel(CVector &, CVector &, CVector &, CVector &, int, float, float, float, char, float *, tWheelState *, ushort) 0x5BA070
/*thiscall*/ float CVehicle::ProcessWheelRotation(tWheelState wheelState, CVector const&, CVector const&, float) 0x5BA900
/*thiscall*/ void CVehicle::RemoveDriver(bool) 0x5B8920
/*thiscall*/ void CVehicle::RemovePassenger(CPed *passenger) 0x5B8CE0
/*thiscall*/ void CVehicle::SetComponentAtomicAlpha(RpAtomic *atomic, int alpha) 0x5B45D0
/*thiscall*/ void CVehicle::SetDriver(CPed *driver) 0x5B89F0
/*thiscall*/ CPed* CVehicle::SetUpDriver(void) 0x5B8870
/*thiscall*/ CPed* CVehicle::SetupPassenger(int) 0x5B8700
/*thiscall*/ bool CVehicle::ShufflePassengersToMakeSpace(void) 0x5B7B10
/*thiscall*/ void CVehicle::UpdateClumpAlpha(void) 0x5B4580
/*thiscall*/ void CVehicle::UpdatePassengerList(void) 0x5B39F0
/*thiscall*/ bool CVehicle::UsesSiren(void) 0x5B8520
/*thiscall*/ void CVehicleModelInfo::AvoidSameVehicleColour(uchar * prim, uchar * sec) 0x579090
/*thiscall*/ int CVehicleModelInfo::ChooseComponent(void) 0x579670
/*thiscall*/ int CVehicleModelInfo::ChooseSecondComponent(void) 0x5794F0
/*thiscall*/ void CVehicleModelInfo::ChooseVehicleColour(uchar& prim, uchar& sec) 0x579190
/*cdecl*/ RwObject* CVehicleModelInfo::ClearAtomicFlagCB(RwObject* object, void* data) 0x579FD0
/*cdecl*/ RwFrame* CVehicleModelInfo::CollapseFramesCB(RwFrame* frame, void* data) 0x57A660
/*cdecl*/ void CVehicleModelInfo::DeleteVehicleColourTextures(void) 0x578C90
/*thiscall*/ int CVehicleModelInfo::FindEditableMaterialList(void) 0x579390
/*cdecl*/ RpAtomic* CVehicleModelInfo::GetEditableMaterialListCB(RpAtomic* atomic, void* data) 0x579440
/*cdecl*/ RpMaterial* CVehicleModelInfo::GetEditableMaterialListCB(RpMaterial* material, void* data) 0x579460
/*cdecl*/ RpMaterial* CVehicleModelInfo::GetMatFXEffectMaterialCB(RpMaterial* material, void* data) 0x578BA0
/*cdecl*/ int CVehicleModelInfo::GetMaximumNumberOfPassengersFromNumberOfDoors(int modelId) 0x578A70
/*thiscall*/ void CVehicleModelInfo::GetWheelPosn(int wheel, CVector& outVec) 0x579AD0
/*cdecl*/ RpMaterial* CVehicleModelInfo::HasAlphaMaterialCB(RpMaterial * material, void * data) 0x57A600
/*cdecl*/ RpAtomic* CVehicleModelInfo::HideAllComponentsAtomicCB(RpAtomic * atomic, void * data) 0x57A620
/*cdecl*/ void CVehicleModelInfo::LoadEnvironmentMaps(void) 0x578C30
/*cdecl*/ void CVehicleModelInfo::LoadVehicleColours(void) 0x578CC0
/*cdecl*/ RpAtomic* CVehicleModelInfo::MoveObjectsCB(RwObject * object, void * data) 0x57A640
/*thiscall*/ void CVehicleModelInfo::PreprocessHierarchy(void) 0x579B10
/*cdecl*/ RwObject* CVehicleModelInfo::SetAtomicFlagCB(RwObject * object, void * data) 0x579FF0
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetAtomicRendererCB(RpAtomic * atomic, void * data) 0x57A4A0
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetAtomicRendererCB_BigVehicle(RpAtomic * atomic, void * data) 0x57A1E0
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetAtomicRendererCB_Boat(RpAtomic * atomic, void * data) 0x57A070
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetAtomicRendererCB_Heli(RpAtomic * atomic, void * data) 0x57A010
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetAtomicRendererCB_RealHeli(RpAtomic * atomic, void * data) 0x57A300
/*cdecl*/ RpMaterial* CVehicleModelInfo::SetDefaultEnvironmentMapCB(RpMaterial* material, void* data) 0x578B40
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetEnvironmentMapCB(RpAtomic * atomic, void * data) 0x578AF0
/*thiscall*/ void CVehicleModelInfo::SetVehicleColour(uchar prim, uchar sec) 0x579290
/*thiscall*/ void CVehicleModelInfo::SetVehicleComponentFlags(RwFrame* component, uint flags) 0x579E80
/*cdecl*/ void CVehicleModelInfo::ShutdownEnvironmentMaps(void) 0x578BD0
/*thiscall*/ bool CWanted::AddCrimeToQ(eCrimeType crimeType,int,CVector const&,bool,bool) 0x4D1990
/*thiscall*/ bool CWanted::AreArmyRequired(void) 0x4D1E20
/*thiscall*/ bool CWanted::AreFbiRequired(void) 0x4D1E40
/*thiscall*/ bool CWanted::AreMiamiViceRequired(void) 0x4D1E80
/*thiscall*/ bool CWanted::AreSwatRequired(void) 0x4D1E60
/*thiscall*/ void CWanted::CheatWantedLevel(int) 0x4D1F80
/*thiscall*/ void CWanted::ClearQdCrimes(void) 0x4D1A50
/*thiscall*/ void CWanted::Initialise(void) 0x4D2440
/*thiscall*/ bool CWanted::NumOfHelisRequired(void) 0x4D1DE0
/*thiscall*/ void CWanted::RegisterCrime(eCrimeType crimeType,CVector const&,uint,bool) 0x4D20F0
/*thiscall*/ void CWanted::RegisterCrime_Immediately(eCrimeType crimeType,CVector const&,uint,bool) 0x4D20B0
/*thiscall*/ void CWanted::ReportCrimeNow(eCrimeType crimeType,CVector const&,bool) 0x4D1610
/*thiscall*/ void CWanted::Reset(void) 0x4D2420
/*thiscall*/ void CWanted::ResetPolicePursuit(void) 0x4D1D20
/*cdecl*/ void CWanted::SetMaximumWantedLevel(int level) 0x4D1E90
/*thiscall*/ void CWanted::SetWantedLevel(int level) 0x4D1FA0
/*thiscall*/ void CWanted::SetWantedLevelNoDrop(int) 0x4D1F50
/*thiscall*/ void CWanted::Update(void) 0x4D2260
/*thiscall*/ void CWanted::UpdateWantedLevel(void) 0x4D2110
/*cdecl*/ void CWanted::WorkOutPolicePresence(CVector,float) 0x4D1B00
Bool CWeapon::bPhotographHasBeenTaken 0xA10AF4
void __thiscall CWeapon::CWeapon(eWeaponType type, int nAmmoTotal) 0x5D4E20
static void __cdecl CWeapon::InitialiseWeapons(void) 0x5D4DF0
static void __cdecl CWeapon::ShutdownWeapons(void) 0x5D4DD0
static void __cdecl CWeapon::UpdateWeapons(void) 0x5D4DB0
void __thiscall CWeapon::Initialise(eWeaponType type, int nAmmoTotal) 0x5D4D00
void __thiscall CWeapon::Shutdown(void) 0x5D4C90
bool __thiscall CWeapon::Fire(CEntity *pFiringEntity, CVector *vecSourcePos) 0x5D45E0
bool __thiscall CWeapon::FireFromCar(CVehicle *pFiringVehicle, bool bLookLeft, bool bLookRight) 0x5D44E0
bool __thiscall CWeapon::FireMelee(CEntity *pFiringEntity, CVector &veSourcePos) 0x5D2CE0
bool __thiscall CWeapon::FireInstantHit(CEntity *pFiringEntity, CVector *veSourcePos) 0x5D1140
static void __cdecl CWeapon::AddGunFlashBigGuns(CVector vecStart,CVector vecEnd) 0x5D0740
void __thiscall CWeapon::AddGunshell(CEntity *pFiringEntity, CVector const& veSourcePos, CVector2D const& vecDirection, float fSize) 0x5D0560
void __thiscall CWeapon::DoBulletImpact(CEntity *pFiringEntity, CEntity *pCollideEntity, CVector *vecStart, CVector *vecEnd, CColPoint *pColPoint, CVector2D
bool __thiscall CWeapon::FireShotgun(CEntity *pFiringEntity, CVector *vecSourcePos) 0x5CD340
bool __thiscall CWeapon::FireProjectile(CEntity *pFiringEntity, CVector *vecSourcePos, float fForce) 0x5CCF90
bool __thiscall CWeapon::FireAreaEffect(CEntity *pFiringEntity, CVector *vecSourcePos) 0x5CCBB0
bool __thiscall CWeapon::LaserScopeDot(CVector *vecPos, float *fDist) 0x5CC9E0
bool __thiscall CWeapon::FireSniper(CEntity *pFiringEntity) 0x5CC730
bool __thiscall CWeapon::TakePhotograph(CEntity *pFiringEntity) 0x5CC450
bool __thiscall CWeapon::FireM16_1stPerson(CEntity *pFiringEntity) 0x5CBFF0
bool __thiscall CWeapon::FireInstantHitFromCar(CVehicle *pFiringVehicle, bool bLookLeft, bool bLookRight) 0x5CB0A0
static void __cdecl CWeapon::DoDoomAiming(CEntity *pFiringEntity, CVector *vecStart, CVector *vecEnd) 0x5CAD20
static void __cdecl CWeapon::DoTankDoomAiming(CEntity *pFiringEntity1, CEntity *pFiringEntity2, CVector *vecStart, CVector *vecEnd) 0x5CA8B0
static void __cdecl CWeapon::DoDriveByAutoAiming(CEntity *pFiringEntity, CVehicle *pFiringVehicle, CVector *vecStart, CVector *vecEnd) 0x5CA400
void __thiscall CWeapon::Reload(void) 0x5CA3C0
void __thiscall CWeapon::Update(int nAudioEntityId, CPed *pPed) 0x5CA0B0
bool __thiscall CWeapon::IsTypeMelee(void) 0x5C9B90
bool __thiscall CWeapon::IsType2Handed(void) 0x5C9B50
static void __cdecl CWeapon::MakePedsJumpAtShot(CPhysical *pFiringEntity, CVector *vecStart, CVector *vecEnd) 0x5C8C30
static void __cdecl CWeapon::BlowUpExplosiveThings(CEntity *Thing) 0x5C8AE0
bool __thiscall CWeapon::HasWeaponAmmoToBeUsed(void) 0x5C8AB0
static void __cdecl CWeapon::CheckForShootingVehicleOccupant(CEntity **pCollideEntity, CColPoint *pColPoint, eWeaponType type, CVector const& vecStart,
static void __cdecl FireOneInstantHitRound(CVector *vecStart, CVector *vecEnd, int nDamage) 0x5C9BB0
/RwTexture* gpCrossHairTex 0xA0FD40
/CWeaponEffects gCrossHair 0x9786EC
/*thiscall*/ void CWeaponEffects::CWeaponEffects(void) 0x5D5140
/*cdecl*/ void CWeaponEffects::ClearCrossHair(void) 0x5D5050
/*cdecl*/ void CWeaponEffects::Init(void) 0x5D50B0
/*cdecl*/ void CWeaponEffects::MarkTarget(CVector pos, uchar red, uchar green, uchar blue, uchar alpha, float size) 0x5D5060
/*cdecl*/ void CWeaponEffects::Render(void) 0x5D4E90
/*cdecl*/ void CWeaponEffects::Shutdown(void) 0x5D5090
CWeaponInfo aWeaponInfo[37] 0x782A14
/*thiscall*/ void CWeaponInfo::CWeaponInfo(void) 0x5D58D0
/*thiscall*/ void CWeaponInfo::~CWeaponInfo(void) 0x5D58C0
/*cdecl*/ eWeaponFire CWeaponInfo::FindWeaponFireType(char *name) 0x5D5170
/*cdecl*/ CWeaponInfo* CWeaponInfo::GetWeaponInfo(eWeaponType weaponType) 0x5D5710
/*cdecl*/ void CWeaponInfo::Initialise(void) 0x5D5750
/*cdecl*/ void CWeaponInfo::LoadWeaponData(void) 0x5D5250
/*cdecl*/ void CWeaponInfo::Shutdown(void) 0x5D5730
/*thiscall*/ int CWeaponModelInfo::GetWeaponInfo(void) 0x629C20
/*thiscall*/ void CWeaponModelInfo::Init(void) 0x629C70
/*thiscall*/ int CWeaponModelInfo::SetWeaponInfo(int) 0x629C30
/*cdecl*/ void CWeather::AddRain(void) 0x57C900
/*cdecl*/ void CWeather::AddSplashesDuringHurricane(void) 0x57D160
/*cdecl*/ void CWeather::AddStreamAfterRain(void) 0x57D340
/*cdecl*/ void CWeather::ForceWeather(short weather) 0x57D570
/*cdecl*/ void CWeather::ForceWeatherNow(short weather) 0x57D550
/*cdecl*/ void CWeather::Init(void) 0x57E040
/*cdecl*/ void CWeather::ReleaseWeather(void) 0x57D540
/*cdecl*/ void CWeather::RenderRainStreaks(void) 0x57BF40
/*cdecl*/ void CWeather::Update(void) 0x57D580
/CPtrList CWorld::ms_listMovingEntityPtrs 0x9B48A8
/CPtrList CWorld::ms_bigBuildingsList[3] 0x9785FC
/CEntity* CWorld::pIgnoreEntity 0xA10B29
/CSector CWorld::ms_aSectors[6400] 0x792D30
/*cdecl*/ void CWorld::Add(CEntity *entity) 0x4DB3F0
/*cdecl*/ void CWorld::AddParticles(void) 0x4D4BB0
/*cdecl*/ void CWorld::CallOffChaseForArea(float,float,float,float) 0x4D3200
/*cdecl*/ void CWorld::CallOffChaseForAreaSectorListPeds(CPtrList &ptrlist,float,float,float,float,float,float,float,float) 0x4D2DF0
/*cdecl*/ void CWorld::CallOffChaseForAreaSectorListVehicles(CPtrList &ptrlist,float,float,float,float,float,float,float,float) 0x4D2F50
/*cdecl*/ void CWorld::ClearCarsFromArea(float x1,float y1,float z1,float x2,float y2,float z2) 0x4D3700
/*cdecl*/ void CWorld::ClearExcitingStuffFromArea(CVector const&,float,uchar) 0x4D38F0
/*cdecl*/ void CWorld::ClearForRestart(void) 0x4DB4A0
/*cdecl*/ void CWorld::ClearPedsFromArea(float x1,float y1,float z1,float x2,float y2,float z2) 0x4D35C0
/*cdecl*/ void CWorld::ClearScanCodes(void) 0x4D7460
/*cdecl*/ void CWorld::ExtinguishAllCarFiresInArea(CVector position,float radius) 0x4D3480
/*cdecl*/ float CWorld::FindGroundZFor3DCoord(float x,float y,float z,bool *) 0x4D53A0
/*cdecl*/ float CWorld::FindGroundZForCoord(float x,float y) 0x4D5540
/*cdecl*/ int CWorld::FindMissionEntitiesIntersectingCube(CVector const&,CVector const&,short *,short,CEntity **,bool,bool,bool) 0x4D5800
/*cdecl*/ void CWorld::FindMissionEntitiesIntersectingCubeSectorList(CPtrList &ptrlist,CVector const&,CVector const&,short *,short,CEntity **,bool,bool,bool)
/*cdecl*/ int CWorld::FindObjectsInRange(CVector const&,float,bool,short *,short,CEntity **,bool,bool,bool,bool,bool) 0x4D6B90
/*cdecl*/ void CWorld::FindObjectsInRangeSectorList(CPtrList &ptrlist,CVector const&,float,bool,short *,short,CEntity **) 0x4D6AD0
/*cdecl*/ int CWorld::FindObjectsIntersectingAngledCollisionBox(CBox const&,CMatrix const&,CVector const&,float,float,float,float,short *,short,CEntity
/*cdecl*/ void CWorld::FindObjectsIntersectingAngledCollisionBoxSectorList(CPtrList &ptrlist,CBox const&,CMatrix const&,CVector const&,short *,short,CEntity **)
/*cdecl*/ int CWorld::FindObjectsIntersectingCube(CVector const&,CVector const&,short *,short,CEntity **,bool,bool,bool,bool,bool) 0x4D5FB0
/*cdecl*/ void CWorld::FindObjectsIntersectingCubeSectorList(CPtrList &ptrlist,CVector const&,CVector const&,short *,short,CEntity **) 0x4D5EA0
/*cdecl*/ int CWorld::FindObjectsKindaColliding(CVector const&,float,bool,short *,short,CEntity **,bool,bool,bool,bool,bool) 0x4D6370
/*cdecl*/ void CWorld::FindObjectsKindaCollidingSectorList(CPtrList &ptrlist,CVector const&,float,bool,short *,short,CEntity **) 0x4D6280
/*cdecl*/ int CWorld::FindObjectsOfTypeInRange(uint,CVector const&,float,bool,short *,short,CEntity **,bool,bool,bool,bool,bool) 0x4D6770
/*cdecl*/ void CWorld::FindObjectsOfTypeInRangeSectorList(uint,CPtrList &ptrlist,CVector const&,float,bool,short *,short,CEntity **) 0x4D66A0
/*cdecl*/ float CWorld::FindRoofZFor3DCoord(float x,float y,float z,bool *) 0x4D51D0
/*cdecl*/ bool CWorld::GetIsLineOfSightClear(CVector const& origin,CVector const& target,bool,bool,bool,bool,bool,bool,bool) 0x4DA560
/*cdecl*/ bool CWorld::GetIsLineOfSightSectorClear(CSector &,CColLine const& colLine,bool,bool,bool,bool,bool,bool,bool) 0x4D6EC0
/*cdecl*/ void CWorld::Initialise(void) 0x4DB9A0
/*cdecl*/ bool CWorld::IsWanderPathClear(CVector const&,CVector const&,float,int) 0x4D2620
/*cdecl*/ void CWorld::Process(void) 0x4D7500
/*cdecl*/ bool CWorld::ProcessLineOfSight(CVector const& origin,CVector const& target,CColPoint &colPoint,CEntity *&colEntity,bool buildings,bool vehicles,bool
/*cdecl*/ bool CWorld::ProcessLineOfSightSector(CSector &,CColLine const& colLine,CColPoint &colPoint,float &,CEntity *&colEntity,bool buildings,bool
/*cdecl*/ bool CWorld::ProcessLineOfSightSectorList(CPtrList &ptrlist,CColLine const&,CColPoint &colPoint,float &,CEntity *&colEntity,bool,bool,bool) 0x4D8C60
/*cdecl*/ bool CWorld::ProcessVerticalLine(CVector const& origin,float distance,CColPoint &colPoint,CEntity *&colEntity,bool buildings,bool vehicles,bool
/*cdecl*/ bool CWorld::ProcessVerticalLineSector(CSector &,CColLine const& colLine,CColPoint &colPoint,CEntity
/*cdecl*/ void CWorld::Remove(CEntity *entity) 0x4DB310
/*cdecl*/ void CWorld::RemoveFallenCars(void) 0x4D48A0
/*cdecl*/ void CWorld::RemoveFallenPeds(void) 0x4D4A40
/*cdecl*/ void CWorld::RemoveReferencesToDeletedObject(CEntity *entity) 0x4D5090
/*cdecl*/ CBaseModelInfo* CWorld::RepositionCertainDynamicObjects(void) 0x4D4850
/*cdecl*/ CBaseModelInfo* CWorld::RepositionOneObject(CEntity *entity) 0x4D43A0
/*cdecl*/ void CWorld::SetAllCarsCanBeDamaged(bool) 0x4D3550
/*cdecl*/ void CWorld::SetCarsOnFire(float x,float y,float z,float radius,CEntity *vehicles) 0x4D4C30
/*cdecl*/ void CWorld::SetPedsChoking(float x,float y,float z,float radius,CEntity *peds) 0x4D4D90
/*cdecl*/ void CWorld::SetPedsOnFire(float x,float y,float z,float radius,CEntity *peds) 0x4D4F30
/*cdecl*/ void CWorld::ShutDown(void) 0x4DB590
/*cdecl*/ void CWorld::StopAllLawEnforcersInTheirTracks(void) 0x4D25B0
/*cdecl*/ void CWorld::TestSphereAgainstSectorList(CPtrList &ptrlist,CVector,float,CEntity *entity,bool) 0x4D3C40
/*cdecl*/ void CWorld::TestSphereAgainstWorld(CVector,float,CEntity *entity,bool,bool,bool,bool,bool,bool) 0x4D3F40
/*cdecl*/ void CWorld::TriggerExplosion(CVector const&,float,float,CEntity *entity,bool) 0x4D82D0
/*cdecl*/ void CWorld::TriggerExplosionSectorList(CPtrList &ptrlist,CVector const&,float,float,CEntity *entity,bool) 0x4D7B90
/*cdecl*/ void CWorld::UseDetonator(CEntity *entity) 0x4D42F0
/*cdecl*/ char* GetFrameNodeName(RwFrame *frame) 0x580600
/*cdecl*/ char* GetNodeNameFromNodeId(int index) 0x405E70
/*cdecl*/ bool NodeNamePluginAttach(void) 0x580620
/*cdecl*/ int NodeNameStreamGetSize(int) 0x580670
/*cdecl*/ RwStream* NodeNameStreamRead(RwStream *stream, int length, int object) 0x5806A0
/*cdecl*/ RwStream* NodeNameStreamWrite(RwStream *stream, int length, int object) 0x5806D0