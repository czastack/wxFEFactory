/*thiscall*/ void C2deffectsModelInfo::C2deffectsModelInfo(void) 0x50BE60 
/*thiscall*/ void C2deffectsModelInfo::~C2deffectsModelInfo() 0x50BE50 
void CAnimBlendAssociation::~CAnimBlendAssociation() 0x0
/*thiscall*/ void CAnimBlendAssociation::AllocateAnimBlendNodeArray(int) 0x4016A0 
/*thiscall*/ void CAnimBlendAssociation::CAnimBlendAssociation(CAnimBlendAssociation&) 0x4014C0 
/*thiscall*/ void CAnimBlendAssociation::CAnimBlendAssociation(void) 0x401460 
/*thiscall*/ void CAnimBlendAssociation::FreeAnimBlendNodeArray(void) 0x4016F0 
/*thiscall*/ CAnimBlendNode* CAnimBlendAssociation::GetNode(int) 0x4017B0
/*thiscall*/ void CAnimBlendAssociation::Init(CAnimBlendAssociation&) 0x401620 
/*thiscall*/ void CAnimBlendAssociation::Init(RpClump *clump,CAnimBlendHierarchy *hierarchy) 0x401560
/*thiscall*/ void CAnimBlendAssociation::SetBlend(float amount,float delta) 0x4017E0
/*thiscall*/ void CAnimBlendAssociation::SetCurrentTime(float time) 0x401700
/*thiscall*/ void CAnimBlendAssociation::Start(float time) 0x4017D0
/*thiscall*/ void CAnimBlendAssociation::SyncAnimation(CAnimBlendAssociation*) 0x401780 
/*thiscall*/ bool CAnimBlendAssociation::UpdateBlend(float) 0x4032B0 
/*thiscall*/ void CAnimBlendAssociation::UpdateTime(float,float) 0x4031F0 
/*thiscall*/ void CAnimBlendClumpData::CAnimBlendClumpData(void) 0x401880 
/*thiscall*/ void CAnimBlendClumpData::SetNumberOfBones(int) 0x4018F0 
/*thiscall*/ void CAnimBlendClumpData::~CAnimBlendClumpData() 0x4018B0 
/*thiscall*/ void CAnimBlendNode::CalcDeltas(void) 0x401E70 
/*thiscall*/ bool CAnimBlendNode::FindKeyFrame(float) 0x4021B0 
/*thiscall*/ void CAnimBlendNode::GetCurrentTranslation(CVector &,float) 0x401FE0 
/*thiscall*/ void CAnimBlendNode::GetEndTranslation(CVector &,float) 0x402110 
/*thiscall*/ void CAnimBlendNode::Init(void) 0x401B10 
/*thiscall*/ void CAnimBlendNode::NextKeyFrame(void) 0x401DC0 
/*thiscall*/ void CAutomobile::AddDamagedVehicleParticles(void) 0x535450 
/*thiscall*/ bool CAutomobile::AddWheelDirtAndWater(CColPoint &colPoint,uint) 0x5357D0
/*thiscall*/ void CAutomobile::BlowUpCarsInPath(void) 0x53E000 
/*thiscall*/ void CAutomobile::CAutomobile(int modelIndex,uchar createdBy) 0x52C6B0
/*thiscall*/ void CAutomobile::DoDriveByShootings(void) 0x564000 
/*thiscall*/ void CAutomobile::FireTruckControl(void) 0x522590 
/*thiscall*/ void CAutomobile::Fix(void) 0x53C240 
/*thiscall*/ bool CAutomobile::GetAllWheelsOffGround(void) 0x53BC40 
/*thiscall*/ bool CAutomobile::HasCarStoppedBecauseOfLight(void) 0x42E220 
/*thiscall*/ void CAutomobile::HideAllComps(void) 0x5300C0 
/*thiscall*/ void CAutomobile::HydraulicControl(void) 0x52D4E0 
/*thiscall*/ void CAutomobile::PlaceOnRoadProperly(void) 0x53E090 
/*thiscall*/ void CAutomobile::PlayHornIfNecessary(void) 0x53C4B0 
/*thiscall*/ void CAutomobile::ProcessAutoBusDoors(void) 0x53D370 
/*thiscall*/ void CAutomobile::ProcessBuoyancy(void) 0x5308D0 
/*thiscall*/ void CAutomobile::ProcessSwingingDoor(int nodeIndex, eDoors door) 0x535250
/*thiscall*/ bool CAutomobile::RcbanditCheck1CarWheels(CPtrList &ptrlist) 0x53CBA0
/*thiscall*/ bool CAutomobile::RcbanditCheckHitWheels(void) 0x53C990 
/*thiscall*/ void CAutomobile::ReduceHornCounter(void) 0x5308C0 
/*thiscall*/ CObject* CAutomobile::RemoveBonnetInPedCollision(void) 0x535320
/*thiscall*/ void CAutomobile::ResetSuspension(void) 0x5353A0 
/*thiscall*/ void CAutomobile::ScanForCrimes(void) 0x53C4F0 
/*cdecl*/ void CAutomobile::SetAllTaxiLights(bool enable) 0x53C440
/*thiscall*/ void CAutomobile::SetBumperDamage(int nodeIndex,ePanels panel,bool withoutVisualEffect) 0x530120
/*thiscall*/ void CAutomobile::SetBusDoorTimer(uint time,uchar) 0x53D320
/*thiscall*/ void CAutomobile::SetComponentVisibility(RwFrame *frame,uint) 0x5300E0 
/*thiscall*/ void CAutomobile::SetDoorDamage(int nodeIndex, eDoors door, bool withoutVisualEffect) 0x530200
/*thiscall*/ void CAutomobile::SetPanelDamage(int nodeIndex, ePanels panel, bool createWindowGlass) 0x5301A0
/*thiscall*/ void CAutomobile::SetTaxiLight(bool enable) 0x53C420
/*thiscall*/ void CAutomobile::SetupDamageAfterLoad(void) 0x53C310 
/*thiscall*/ void CAutomobile::SetupModelNodes(void) 0x52D1B0 
/*thiscall*/ void CAutomobile::SetupSuspensionLines(void) 0x52D210 
/*thiscall*/ void CAutomobile::ShowAllComps(void) 0x5300D0 
/*thiscall*/ CObject* CAutomobile::SpawnFlyingComponent(int nodeIndex, uint collisionType) 0x530300
/*thiscall*/ void CAutomobile::TankControl(void) 0x53D530 
/*thiscall*/ void CAutomobile::VehicleDamage(float damageIntensity,ushort) 0x52F390
/*thiscall*/ void CAutomobile::dmgDrawCarCollidingParticles(CVector const& position, float force) 0x52F030
/*thiscall*/ void CAutoPilot::ModifySpeed(float) 0x4137B0 
/*thiscall*/ void CAutoPilot::RemoveOnePathNode(void) 0x413A00 
void CBaseModelInfo::Shutdown(void) 0x0
/*thiscall*/ void CBaseModelInfo::Add2dEffect(C2dEffect *effect) 0x4F6B20
/*thiscall*/ void CBaseModelInfo::AddRef(void) 0x4F6BA0 
/*thiscall*/ void CBaseModelInfo::AddTexDictionaryRef(void) 0x4F6B80 
/*thiscall*/ void CBaseModelInfo::ClearTexDictionary(void) 0x4F6B70 
/*thiscall*/ void CBaseModelInfo::DeleteCollisionModel(void) 0x4F6AC0 
/*thiscall*/ C2dEffect* CBaseModelInfo::Get2dEffect(int effectNumber) 0x4F6B00
/*thiscall*/ void CBaseModelInfo::Init2dEffects(void) 0x4F6AF0 
/*thiscall*/ void CBaseModelInfo::RemoveRef(void) 0x4F6BB0 
/*thiscall*/ void CBaseModelInfo::RemoveTexDictionaryRef(void) 0x4F6B90 
/*thiscall*/ void CBaseModelInfo::SetTexDictionary(char const*txdName) 0x4F6B40
/*thiscall*/ void CBoat::AddWakePoint(CVector posn) 0x542140
/*thiscall*/ void CBoat::ApplyWaterResistance(void) 0x541A30 
/*thiscall*/ void CBoat::CBoat(int modelIndex, uchar createdBy) 0x53E3E0
/*cdecl*/ void CBoat::FillBoatList(void) 0x542250
/*cdecl*/ bool CBoat::IsSectorAffectedByWake(CVector2D,float,CBoat**) 0x542370
/*cdecl*/ float CBoat::IsVertexAffectedByWake(CVector,CBoat*) 0x5424A0
/*thiscall*/ void CBoat::PruneWakeTrail(void) 0x5420D0 
/*thiscall*/ void CBoat::SetupModelNodes(void) 0x53E7D0 
/*cdecl*/ RwObject* GetBoatAtomicObjectCB(RwObject *object,void *data) 0x53E3C0
CTreadable* CBuilding::GetIsATreadable(void) 0x0
/*thiscall*/ void CBuilding::CBuilding(void) 0x4057D0
/*thiscall*/ void CBuilding::ReplaceWithNewModel(int modelIndex) 0x405850
/*cdecl*/ void* CBuilding::operator new(uint size) 0x405820
/*cdecl*/ void CBuilding::operator delete(void *data) 0x405830
/*thiscall*/ uint CCarGenerator::CalcNextGen(void) 0x5426C0 
/*thiscall*/ bool CCarGenerator::CheckForBlockage(void) 0x542DF0 
/*thiscall*/ bool CCarGenerator::CheckIfWithinRangeOfAnyPlayers(void) 0x542E50 
/*thiscall*/ void CCarGenerator::DoInternalProcessing(void) 0x5426E0 
/*thiscall*/ void CCarGenerator::Process(void) 0x542BB0 
/*thiscall*/ void CCarGenerator::Setup(float x,float y,float z,float angle,int modelId,short primaryColor,short secondaryColor,uchar forceSpawn,uchar alarm,uchar 
/*thiscall*/ void CCarGenerator::SwitchOff(void) 0x542690 
/*thiscall*/ void CCarGenerator::SwitchOn(void) 0x5426A0 
/*cdecl*/ void CCheat::WeaponCheat(void) 0x490D90 
/*cdecl*/ void CCheat::HealthCheat(void) 0x490E70 
/*cdecl*/ void CCheat::TankCheat(void) 0x490EE0 
/*cdecl*/ void CCheat::BlowUpCarsCheat(void) 0x491040 
/*cdecl*/ void CCheat::ChangePlayerCheat(void) 0x4910B0 
/*cdecl*/ void CCheat::MayhemCheat(void) 0x4911C0 
/*cdecl*/ void CCheat::EverybodyAttacksPlayerCheat(void) 0x491270 
/*cdecl*/ void CCheat::WeaponsForAllCheat(void) 0x491370 
/*cdecl*/ void CCheat::FastTimeCheat(void) 0x4913A0 
/*cdecl*/ void CCheat::SlowTimeCheat(void) 0x4913F0 
/*cdecl*/ void CCheat::MoneyCheat(void) 0x491430 
/*cdecl*/ void CCheat::ArmourCheat(void) 0x491460 
/*cdecl*/ void CCheat::WantedLevelUpCheat(void) 0x491490 
/*cdecl*/ void CCheat::WantedLevelDownCheat(void) 0x4914F0 
/*cdecl*/ void CCheat::SunnyWeatherCheat(void) 0x491520 
/*cdecl*/ void CCheat::CloudyWeatherCheat(void) 0x491550 
/*cdecl*/ void CCheat::RainyWeatherCheat(void) 0x491580 
/*cdecl*/ void CCheat::FoggyWeatherCheat(void) 0x4915B0 
/*cdecl*/ void CCheat::FastWeatherCheat(void) 0x4915E0 
/*cdecl*/ void CCheat::OnlyRenderWheelsCheat(void) 0x491610 
/*cdecl*/ void CCheat::ChittyChittyBangBangCheat(void) 0x491640 
/*cdecl*/ void CCheat::StrongGripCheat(void) 0x491670 
/*cdecl*/ void CCheat::NastyLimbsCheat(void) 0x4916A0 
/*thiscall*/ void CCivilianPed::CCivilianPed(ePedType pedType,uint modelIndex) 0x4BFF30
/*thiscall*/ void CCivilianPed::CivilianAI(void) 0x4C07A0 
/*cdecl*/ std::uint16_t CClock::GetGameClockMinutesUntil(unsigned char hours, unsigned char minutes) 0x4733F0
/*cdecl*/ bool CClock::GetIsTimeInRange(unsigned char hourA, unsigned char hourB) 0x473420
/*cdecl*/ void CClock::Initialise(std::uint32_t milisecondsPerGameMinute) 0x473370
/*cdecl*/ void CClock::RestoreClock(void) 0x473570 
/*cdecl*/ void CClock::SetGameClock(unsigned char hours, unsigned char minutes) 0x4733C0
/*cdecl*/ void CClock::StoreClock(void) 0x473540 
/*cdecl*/ void CClock::Update(void) 0x473460 
/*cdecl*/ void CClouds::Init(void) 0x4F6C10 
/*cdecl*/ void CClouds::Render(void) 0x4F6D90 
/*cdecl*/ void CClouds::RenderBackground(short redTop,short greenTop,short blueTop,short redBottom,short greenBottom,short blueBottom,short alpha) 0x4F7F00
/*cdecl*/ void CClouds::RenderHorizon(void) 0x4F85F0 
/*cdecl*/ void CClouds::Shutdown(void) 0x4F6CA0 
/*cdecl*/ void CClouds::Update(void) 0x4F6CE0 
void CClumpModelInfo::DeleteRwObject(void) 0x4F8800
void CClumpModelInfo::CreateInstance(void) 0x4F8920
void CClumpModelInfo::CreateInstance(RwMatrixTag *) 0x4F88A0
void CClumpModelInfo::GetRwObject(void) 0x50C1C0
void CClumpModelInfo::SetClump(RpClump *clump) 0x4F8830
/*thiscall*/ void CClumpModelInfo::CClumpModelInfo(void) 0x50C040 
/*cdecl*/ void CClumpModelInfo::FillFrameArray(RpClump *clump,RwFrame **frames) 0x4F8B90
/*cdecl*/ void CClumpModelInfo::FillFrameArrayCB(RwFrame *frame,void *searchData) 0x4F8B20
/*cdecl*/ RwFrame* CClumpModelInfo::FindFrameFromIdCB(RwFrame *frame,void *searchData) 0x4F8AD0
/*cdecl*/ RwFrame* CClumpModelInfo::FindFrameFromNameCB(RwFrame *frame,void *searchData) 0x4F8960
/*cdecl*/ RwFrame* CClumpModelInfo::FindFrameFromNameWithoutIdCB(RwFrame *frame,void *searchData) 0x4F8A10
/*cdecl*/ RwFrame* CClumpModelInfo::GetFrameFromId(RpClump *clump,int id) 0x4F8B50
/*cdecl*/ void CClumpModelInfo::SetAtomicRendererCB(RpAtomic *atomic,void *renderFunc) 0x4F8940
/*thiscall*/ void CClumpModelInfo::SetFrameIds(RwObjectNameIdAssocation *data) 0x4F8BB0
/*thiscall*/ void CColBox::Set(CVector const& sup, CVector const& inf, uchar material, uchar flags) 0x40B2A0
/*thiscall*/ void CColBox::operator=(CColBox const& right) 0x40B2E0
/*thiscall*/ void CColLine::CColLine(CVector const& start, CVector const& end) 0x40B320
/*thiscall*/ void CColLine::Set(CVector const& start, CVector const& end) 0x40B350
/*thiscall*/ void CColModel::CColModel(void) 0x411680
/*thiscall*/ void CColModel::CalculateTrianglePlanes(void) 0x411CB0
/*thiscall*/ int CColModel::GetLinkPtr(void) 0x411D60
/*thiscall*/ int CColModel::GetTrianglePoint(CVector &, int) 0x411C70
/*thiscall*/ void CColModel::RemoveCollisionVolumes(void) 0x411D80
/*thiscall*/ void CColModel::RemoveTrianglePlanes(void) 0x411D10
/*thiscall*/ void CColModel::operator=(CColModel const&) 0x411710
/*thiscall*/ void CColModel::~CColModel() 0x4116E0
/*thiscall*/ void CColModel::SetLinkPtr(CLink<CColModel*> *) 0x411D40
/*thiscall*/ void CColSphere::Set(float radius, CVector const& center, uchar material, uchar flags) 0x411E40
/*thiscall*/ void CColTriangle::Set(CompressedVector const*,int,int,int,uchar,uchar) 0x411E70
/*thiscall*/ void CColTrianglePlane::Set(CompressedVector const*,CColTriangle &) 0x411EA0 
/*thiscall*/ void CColTrianglePlane::GetNormal(CVector &) 0x412140 
/*thiscall*/ void CControllerState::Clear(void) 0x4916C0
/*thiscall*/ void CCopPed::ArrestPlayer(void) 0x4C2C90
/*thiscall*/ void CCopPed::CCopPed(eCopType copType) 0x4C11B0
/*thiscall*/ void CCopPed::ClearPursuit(void) 0x4C28C0
/*thiscall*/ void CCopPed::CopAI(void) 0x4C1B50
/*thiscall*/ int CCopPed::ScanForCrimes(void) 0x4C26A0
/*thiscall*/ void CCopPed::SetArrestPlayer(CPed * ped) 0x4C2B00
/*thiscall*/ void CCopPed::SetPursuit(bool) 0x4C27D0
/*thiscall*/ void CCurrentVehicle::CCurrentVehicle(void) 0x4AD5E0 
/*thiscall*/ void CCurrentVehicle::Display(void) 0x4AD630 
/*thiscall*/ void CCurrentVehicle::Init(void) 0x4AD5F0 
/*thiscall*/ void CCurrentVehicle::Process(void) 0x4AD600 
/*thiscall*/ void CCutsceneHead::PlayAnimation(char const* name) 0x4BA6A0 
/*thiscall*/ void CCutsceneHead::CCutsceneHead(CObject *object) 0x4BA5E0
/*thiscall*/ void CCutsceneObject::CCutsceneObject(void) 0x4BA910
/*thiscall*/ bool CDamageManager::ApplyDamage(tComponent component, float intensity, float) 0x545A80
/*thiscall*/ void CDamageManager::FuckCarCompletely(void) 0x545B70 
/*thiscall*/ bool CDamageManager::GetComponentGroup(tComponent component, tComponentGroup* group, uchar *damageCompId) 0x545790 
/*thiscall*/ uint CDamageManager::GetDoorStatus(eDoors door) 0x545930
/*thiscall*/ uint CDamageManager::GetEngineStatus(void) 0x545960
/*thiscall*/ uint CDamageManager::GetLightStatus(eLights light) 0x545890
/*thiscall*/ uint CDamageManager::GetPanelStatus(ePanels panel) 0x5458E0 
/*thiscall*/ uint CDamageManager::GetWheelStatus(int wheel) 0x545910
/*thiscall*/ bool CDamageManager::ProgressDoorDamage(uchar door) 0x545970 
/*thiscall*/ bool CDamageManager::ProgressEngineDamage(float damage) 0x5459B0
/*thiscall*/ bool CDamageManager::ProgressWheelDamage(uchar wheel) 0x545A40
/*thiscall*/ bool CDamageManager::ProgressPanelDamage(uchar panel) 0x545A00
/*thiscall*/ void CDamageManager::ResetDamageStatus(void) 0x545850 
/*thiscall*/ void CDamageManager::SetDoorStatus(eDoors door, uint status) 0x545920
/*thiscall*/ void CDamageManager::SetEngineStatus(uint status) 0x545940
/*thiscall*/ void CDamageManager::SetWheelStatus(int wheel, uint status) 0x545900
/*thiscall*/ void CDamageManager::SetLightStatus(eLights light,uint status) 0x545860
/*thiscall*/ void CDamageManager::SetPanelStatus(int panel,uint status) 0x5458B0
/*thiscall*/ void CDirectory::CDirectory(int capacity) 0x4735C0
/*thiscall*/ void CDirectory::~CDirectory() 0x4735F0
/*thiscall*/ void CDirectory::AddItem(DirectoryInfo const&entry) 0x473600
/*thiscall*/ void CDirectory::ReadDirFile(char const*filename) 0x473630
/*thiscall*/ bool CDirectory::WriteDirFile(char const*filename) 0x473690
/*thiscall*/ DirectoryInfo* CDirectory::FindItem(char const*name,uint &outOffset,uint &outSize) 0x4736E0
/*thiscall*/ void CDoor::CDoor(void) 0x52D150
/*thiscall*/ float CDoor::GetAngleOpenRatio(void) 0x545F80
/*thiscall*/ bool CDoor::IsClosed(void) 0x546060
/*thiscall*/ bool CDoor::IsFullyOpen(void) 0x546090
/*thiscall*/ void CDoor::Open(float angle) 0x545EF0
/*thiscall*/ void CDoor::Process(CVehicle *vehicle) 0x545BD0
/*thiscall*/ float CDoor::RetAngleWhenClosed(void) 0x545FE0
/*thiscall*/ float CDoor::RetAngleWhenOpen(void) 0x546020
/*thiscall*/ void CDummy::CDummy(void) 0x4737E0
/*cdecl*/ void* CDummy::operator new(uint size) 0x473830
/*cdecl*/ void CDummy::operator delete(void *data) 0x473840
/*thiscall*/ void CDummyObject::CDummyObject(CObject *object) 0x4BAB10
/*thiscall*/ void CDummyObject::CDummyObject(void) 0x4BAAF0
/*thiscall*/ void CEmergencyPed::CEmergencyPed(uint modelIndex) 0x4C2E40
/*thiscall*/ void CEmergencyPed::FiremanAI(void) 0x4C3CE0 
/*thiscall*/ bool CEmergencyPed::InRange(CPed *ped) 0x4C3EC0 
/*thiscall*/ void CEmergencyPed::MedicAI(void) 0x4C30A0 
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
/*cdecl*/ void CEntity::AddSteamsFromGround(CVector *) 0x4B3FE0
/*thiscall*/ void CEntity::AttachToRwObject(RwObject *rwObject) 0x473F10
/*thiscall*/ void CEntity::CEntity(void) 0x473C30
/*thiscall*/ void CEntity::DetachFromRwObject(void) 0x473F60
/*thiscall*/ void CEntity::GetBoundCentre(CVector &out) 0x4742C0
/*thiscall*/ CVector CEntity::GetBoundCentre(void) 0x474290
/*thiscall*/ float CEntity::GetBoundRadius(void) 0x474310
/*thiscall*/ float CEntity::GetDistanceFromCentreOfMassToBaseOfModel(void) 0x4755C0
/*thiscall*/ bool CEntity::GetIsOnScreen(void) 0x474CC0
/*thiscall*/ bool CEntity::GetIsOnScreenComplex(void) 0x474D20
/*thiscall*/ bool CEntity::GetIsTouching(CVector const&posn, float radius) 0x474C10
/*thiscall*/ bool CEntity::IsVisible(void) 0x474CA0
/*thiscall*/ void CEntity::ModifyMatrixForBannerInWind(void) 0x475830
/*thiscall*/ void CEntity::ModifyMatrixForTreeInWind(void) 0x475670
/*thiscall*/ void CEntity::PreRenderForGlassWindow(void) 0x475A20
/*thiscall*/ void CEntity::ProcessLightsForEntity(void) 0x4FA530
/*thiscall*/ void CEntity::PruneReferences(void) 0x4A7530
/*thiscall*/ void CEntity::RegisterReference(CEntity** entity) 0x4A7480
/*thiscall*/ void CEntity::ResolveReferences(void) 0x4A74E0
/*thiscall*/ void CEntity::SetupBigBuilding(void) 0x4755E0
/*thiscall*/ void CEntity::UpdateRwFrame(void) 0x474330
/*cdecl*/ void CEntryInfoNode::operator delete(void *data) 0x475A50
/*cdecl*/ void* CEntryInfoNode::operator new(uint size) 0x475A40
/*thiscall*/ void CEntryInfoList::Flush(void) 0x475A70
/*cdecl*/ char* CFileLoader::LoadLine(int fileHandle) 0x4761D0
/*cdecl*/ char* GetFilename(char const* filepath) 0x476230
/*cdecl*/ void LoadingScreenLoadingFile(char const* filepath) 0x476250
/*cdecl*/ void CFileLoader::LoadLevel(char const* datFilePath) 0x476290
/*cdecl*/ void CFileLoader::LoadCollisionFromDatFile(uint gameLevel) 0x476520
/*cdecl*/ void CFileLoader::LoadTexDictionary(char const* filepath) 0x4765B0
/*cdecl*/ RwTexture* MoveTexturesCB(RwTexture *texture,void *data) 0x476610
/*cdecl*/ void CFileLoader::AddTexDictionaries(RwTexDictionary *dst,RwTexDictionary *src) 0x476630
/*cdecl*/ void GetNameAndLOD(char *nodeName, char *outName, uint *outLodIndex) 0x476650
/*cdecl*/ RpAtomic* CFileLoader::FindRelatedModelInfoCB(RpAtomic *atomic,void *data) 0x4766C0
/*cdecl*/ void CFileLoader::LoadAtomicFile(char const* filepath) 0x476750
/*cdecl*/ RpClump* CFileLoader::LoadAtomicFile2Return(char const* filepath) 0x4767C0
/*cdecl*/ void CFileLoader::LoadClumpFile(char const* filepath) 0x476810
/*cdecl*/ RpAtomic* CFileLoader::SetRelatedModelInfoCB(RpAtomic *atomic,void *data) 0x4768C0
/*cdecl*/ bool CFileLoader::LoadAtomicFile(RwStream *stream,uint modelIndex) 0x476930
/*cdecl*/ bool CFileLoader::LoadClumpFile(RwStream *stream,uint modelIndex) 0x476990
/*cdecl*/ bool CFileLoader::StartLoadClumpFile(RwStream *stream,uint modelIndex) 0x476A20
/*cdecl*/ bool CFileLoader::FinishLoadClumpFile(RwStream *stream,uint modelIndex) 0x476A70
/*cdecl*/ void CFileLoader::LoadObjectTypes(char const* filepath) 0x476AC0
/*cdecl*/ void CFileLoader::ReloadPaths(char const* filepath) 0x476DB0
/*cdecl*/ void CFileLoader::ReloadObjectTypes(char const* filepath) 0x476F30
/*cdecl*/ void CFileLoader::LoadObject(char const* line) 0x477040
/*cdecl*/ void CFileLoader::ReloadObject(char const* line) 0x4772B0
/*cdecl*/ void CFileLoader::LoadTimeObject(char const* line) 0x4774B0
/*cdecl*/ void CFileLoader::LoadMLO(char const* line) 0x477750
/*cdecl*/ void CFileLoader::LoadMLOInstance(int modelIndex,char const* line) 0x4777C0
/*cdecl*/ void CFileLoader::LoadClumpObject(char const* line) 0x477920
/*cdecl*/ void CFileLoader::LoadVehicleObject(char const* line) 0x477990
/*cdecl*/ void CFileLoader::LoadPedObject(char const* line) 0x477DE0
/*cdecl*/ int CFileLoader::LoadPathHeader(char const* line,char *outPathType) 0x477ED0
/*cdecl*/ void CFileLoader::LoadPedPathNode(char const* line,int id,int index) 0x477F00
/*cdecl*/ void CFileLoader::LoadCarPathNode(char const* line,int id,int index) 0x477FF0
/*cdecl*/ void CFileLoader::Load2dEffect(char const* line) 0x4780E0
/*cdecl*/ void CFileLoader::LoadScene(char const* filepath) 0x478370
/*cdecl*/ void CFileLoader::LoadMapZones(char const* filepath) 0x478550
/*cdecl*/ void CFileLoader::LoadObjectInstance(char const* line) 0x4786B0
/*cdecl*/ void CFileLoader::LoadPickup(char const* line) 0x4789C0
/*cdecl*/ void CFileLoader::LoadZone(char const* line) 0x478A00
/*cdecl*/ void CFileLoader::LoadCullZone(char const* line) 0x478A90
/*cdecl*/ void CFileLoader::LoadCollisionFile(char *filepath) 0x478B20
/*cdecl*/ void CFileLoader::LoadCollisionModel(uchar *buffer,CColModel &outColModel,char *name) 0x478C20
/*cdecl*/ void CFileMgr::Initialise(void) 0x478F80
/*cdecl*/ void CFileMgr::ChangeDir(char const*dir) 0x478FB0
/*cdecl*/ void CFileMgr::SetDir(char const*dir) 0x479020
/*cdecl*/ void CFileMgr::SetDirMyDocuments(void) 0x479080
/*cdecl*/ int CFileMgr::LoadTextFile(char const*filepath,uchar *buffer,int size, char const*mode) 0x479090
/*cdecl*/ int CFileMgr::OpenFile(char const*filepath,char const*mode) 0x479100
/*cdecl*/ int CFileMgr::OpenFileForWriting(char const*filepath) 0x479120
/*cdecl*/ int CFileMgr::Read(int fileHandle,char *buffer,int size) 0x479140
/*cdecl*/ int CFileMgr::Write(int fileHandle,char *buffer,int size) 0x479160
/*cdecl*/ bool CFileMgr::Seek(int fileHandle,int offset,int origin) 0x479180
/*cdecl*/ bool CFileMgr::ReadLine(int fileHandle,char *buffer,int maxSize) 0x4791D0
/*cdecl*/ int CFileMgr::CloseFile(int fileHandle) 0x479200
/*cdecl*/ int CFileMgr::GetErrorReadWrite(int fileHandle) 0x479210
/*cdecl*/ void CFont::DrawFonts(void) 0x501B50 
/*cdecl*/ wchar_t* CFont::GetNextSpace(wchar_t *str) 0x501960
/*cdecl*/ int CFont::GetNumberLines(float x,float y,wchar_t *text) 0x501260
/*cdecl*/ float CFont::GetStringWidth(wchar_t *str,bool sentence) 0x5018A0
/*cdecl*/ CRect* CFont::GetTextRect(CRect *rect_out,float x,float y,wchar_t *text) 0x5013B0
/*cdecl*/ void CFont::InitPerFrame(void) 0x500BE0 
/*cdecl*/ void CFont::Initialise(void) 0x500A40 
/*cdecl*/ wchar_t* CFont::ParseToken(wchar_t *str) 0x5019A0
/*cdecl*/ void CFont::PrintChar(float x,float y,short character) 0x500C30
/*cdecl*/ void CFont::PrintString(float x,float y,wchar_t *text) 0x500F50
/*cdecl*/ void CFont::PrintString(float x,float y,wchar_t *str1,wchar_t *str2,float) 0x501730
/*cdecl*/ void CFont::SetAlphaFade(float alpha) 0x501DD0
/*cdecl*/ void CFont::SetBackGroundOnlyTextOff(void) 0x501D40 
/*cdecl*/ void CFont::SetBackGroundOnlyTextOn(void) 0x501D30 
/*cdecl*/ void CFont::SetBackgroundColor(CRGBA color) 0x501D00 
/*cdecl*/ void CFont::SetBackgroundOff(void) 0x501CF0 
/*cdecl*/ void CFont::SetBackgroundOn(void) 0x501CE0 
/*cdecl*/ void CFont::SetCentreOff(void) 0x501CB0 
/*cdecl*/ void CFont::SetCentreOn(void) 0x501C90 
/*cdecl*/ void CFont::SetCentreSize(float size) 0x501CD0
/*cdecl*/ void CFont::SetColor(CRGBA color) 0x501BD0
/*cdecl*/ void CFont::SetDropColor(CRGBA color) 0x501DE0
/*cdecl*/ void CFont::SetDropShadowPosition(short value) 0x501E70
/*cdecl*/ void CFont::SetFontStyle(short style) 0x501DB0
/*cdecl*/ void CFont::SetJustifyOff(void) 0x501C80 
/*cdecl*/ void CFont::SetJustifyOn(void) 0x501C60 
/*cdecl*/ void CFont::SetPropOff(void) 0x501D90 
/*cdecl*/ void CFont::SetPropOn(void) 0x501DA0 
/*cdecl*/ void CFont::SetRightJustifyOff(void) 0x501D70 
/*cdecl*/ void CFont::SetRightJustifyOn(void) 0x501D50 
/*cdecl*/ void CFont::SetRightJustifyWrap(float value) 0x501DC0
/*cdecl*/ void CFont::SetScale(float width,float height) 0x501B80
/*cdecl*/ void CFont::SetSlant(float value) 0x501BC0
/*cdecl*/ void CFont::SetSlantRefPoint(float x,float y) 0x501BA0 
/*cdecl*/ void CFont::SetWrapx(float value) 0x501CC0
/*cdecl*/ void CFont::Shutdown(void) 0x500BA0 
/*cdecl*/ short CFont::character_code(uchar character) 0x501E80
/*cdecl*/ void AsciiToUnicode(char const* str_ascii,wchar_t * str_unicode) 0x5009C0
/*cdecl*/ int UnicodeStrlen(wchar_t const* str) 0x500A20 
/*cdecl*/ char* UnicodeToAscii(wchar_t *str_unicode) 0x52C2F0
/*thiscall*/ void CFontDetails::~CFontDetails() 0x501F10
/*cdecl*/ float CGeneral::GetATanOfXY(float x,float y) 0x48CC30 
/*cdecl*/ float CGeneral::GetAngleBetweenPoints(float x1,float y1,float x2,float y2) 0x48CA30 
/*cdecl*/ int CGeneral::GetNodeHeadingFromVector(float x,float y) 0x48CE40 
/*cdecl*/ float CGeneral::GetRadianAngleBetweenPoints(float x1,float y1,float x2,float y2) 0x48CA50 
/*cdecl*/ float CGeneral::LimitAngle(float angle) 0x48CB40
/*cdecl*/ float CGeneral::LimitRadianAngle(float angle) 0x48CB90
/*cdecl*/ void CHeli::ActivateHeli(bool enable) 0x54A940
/*thiscall*/ void CHeli::CHeli(int modelIndex, uchar createdBy) 0x547220
/*cdecl*/ void CHeli::CatalinaTakeOff(void) 0x54A9B0
/*cdecl*/ void CHeli::FindPointerToCatalinasHeli(void) 0x54AA20
/*cdecl*/ bool CHeli::HasCatalinaBeenShotDown(void) 0x54AA10
/*cdecl*/ void CHeli::InitHelis(void) 0x549970
/*cdecl*/ void CHeli::MakeCatalinaHeliFlyAway(void) 0x54A9C0
/*thiscall*/ void CHeli::PreRenderAlways(void) 0x5477F0 
/*cdecl*/ void CHeli::RemoveCatalinaHeli(void) 0x54A9D0
/*thiscall*/ CObject* CHeli::SpawnFlyingComponent(int nodeIndex) 0x54AE50
/*cdecl*/ void CHeli::SpecialHeliPreRender(void) 0x54AE10
/*cdecl*/ bool CHeli::TestBulletCollision(CVector *,CVector *,CVector *,int) 0x54AB30
/*cdecl*/ bool CHeli::TestRocketCollision(CVector *) 0x54AA30
/*cdecl*/ void CHeli::UpdateHelis(void) 0x5499F0
/*cdecl*/ void GenerateHeli(bool enable) 0x54A640
/*cdecl*/ void StartCatalinaFlyBy(void) 0x54A980
/*cdecl*/ RwObject* GetHeliAtomicObjectCB(RwObject* object, void* data) 0x54AE30
/*cdecl*/ void CIniFile::LoadIniFile(void) 0x59BE20
/*thiscall*/ void CInstance::CInstance(void) 0x50BEB0 
/*thiscall*/ void CInstance::Shutdown(void) 0x50B850 
/*thiscall*/ void CKeyboardState::Clear(void) 0x491760
/*cdecl*/ void CLines::RenderLineWithClipping(float x1,float y1,float z1,float x2,float y2,float z2,uint,uint) 0x50A3B0
/*thiscall*/ void CMatrix::Attach(RwMatrixTag *rwMatrix,bool deleteOnDetach) 0x4B8DD0
/*thiscall*/ void CMatrix::AttachRW(RwMatrixTag *rwMatrix,bool deleteOnDetach) 0x4B8E00
/*thiscall*/ void CMatrix::CMatrix(CMatrix const&src) 0x4B8D70
/*thiscall*/ void CMatrix::CMatrix(RwMatrixTag *rwMatrix,bool deleteOnDetach)0x4B8D90
/*thiscall*/ void CMatrix::CopyOnlyMatrix(CMatrix const&src) 0x4B8F70
/*thiscall*/ void CMatrix::Detach(void) 0x4B8E30
/*thiscall*/ void CMatrix::Reorthogonalise(void) 0x4B9A80
/*thiscall*/ void CMatrix::ResetOrientation(void) 0x4B9070
/*thiscall*/ void CMatrix::Rotate(float x,float y,float z) 0x4B9770
/*thiscall*/ void CMatrix::RotateX(float angle) 0x4B9510
/*thiscall*/ void CMatrix::RotateZ(float angle) 0x4B9640
/*thiscall*/ void CMatrix::SetRotate(float x,float y,float z) 0x4B93A0
/*thiscall*/ void CMatrix::SetRotateX(float angle) 0x4B9310
/*thiscall*/ void CMatrix::SetRotateXOnly(float angle) 0x4B9160
/*thiscall*/ void CMatrix::SetRotateY(float angle) 0x4B9340
/*thiscall*/ void CMatrix::SetRotateYOnly(float angle) 0x4B91F0
/*thiscall*/ void CMatrix::SetRotateZ(float angle) 0x4B9370
/*thiscall*/ void CMatrix::SetRotateZOnly(float angle) 0x4B9280
/*thiscall*/ void CMatrix::SetScale(float factor) 0x4B90B0
/*thiscall*/ void CMatrix::SetTranslate(float x,float y,float z) 0x4B9100
/*thiscall*/ void CMatrix::SetUnity(void) 0x4B9010
/*thiscall*/ void CMatrix::Update(void) 0x4B8E50
/*thiscall*/ void CMatrix::UpdateRW(void) 0x4B8EC0
/*thiscall*/ void CMatrix::operator+=(CMatrix const&right) 0x4B8F90
/*thiscall*/ void CMatrix::operator=(CMatrix const&right) 0x4B8F40
/*thiscall*/ void CMatrix::~CMatrix() 0x4B8DB0
/*cdecl*/ CMatrix operator*(CMatrix const&a,CMatrix const&b) 0x4B9D60
/*cdecl*/ void Invert(CMatrix const&in,CMatrix&out) 0x4B9C30
/*cdecl*/ CMatrix Invert(CMatrix const&in) 0x4B9BF0
/*cdecl*/ CVector operator*(CMatrix const&m,CVector const&v) 0x4BA4D0
/*cdecl*/ CVector Multiply3x3(CVector const&v,CMatrix const&m) 0x4BA450
/*cdecl*/ CVector Multiply3x3(CMatrix const&m,CVector const&v) 0x4BA3D0
/*cdecl*/ void CMessages::Init(void) 0x529310
/*cdecl*/ int CMessages::GetWideStringLength(ushort *str) 0x529490
/*cdecl*/ int CMessages::WideStringCopy(ushort *dst,ushort *src,ushort size) 0x5294B0
/*cdecl*/ bool CMessages::WideStringCompare(ushort *str1,ushort *str2,ushort size) 0x529510
/*cdecl*/ void CMessages::Process(void) 0x529580
/*cdecl*/ void CMessages::Display(void) 0x529800
/*cdecl*/ void CMessages::AddMessage(ushort *text,uint time,ushort flag) 0x529900
/*cdecl*/ void CMessages::AddMessageJumpQ(ushort *text,uint time,ushort flag) 0x529A10
/*cdecl*/ void CMessages::AddMessageSoon(ushort *text,uint time,ushort flag) 0x529AF0
/*cdecl*/ void CMessages::ClearMessages(void) 0x529CE0
/*cdecl*/ void CMessages::ClearSmallMessagesOnly(void) 0x529E00
/*cdecl*/ void CMessages::AddBigMessage(ushort *text,uint time,ushort flag) 0x529EB0
/*cdecl*/ void CMessages::AddBigMessageQ(ushort *text,uint time,ushort flag) 0x529F60
/*cdecl*/ void CMessages::AddToPreviousBriefArray(ushort *text, int n1, int n2, int n3, int n4, int n5, int n6,ushort *str) 0x52A040
/*cdecl*/ void CMessages::InsertNumberInString(ushort *src, int n1, int n2, int n3, int n4, int n5, int n6,ushort *dst) 0x52A1A0
/*cdecl*/ void CMessages::InsertStringInString(ushort *text,ushort *str) 0x52A300
/*cdecl*/ void CMessages::InsertPlayerControlKeysInString(ushort *text) 0x52A490
/*cdecl*/ void CMessages::AddMessageWithNumber(ushort *text,uint time,ushort flag,int n1,int n2,int n3,int n4,int n5,int n6) 0x52A850
/*cdecl*/ void CMessages::AddMessageJumpQWithNumber(ushort *text,uint time,ushort flag, int n1, int n2, int n3, int n4, int n5, int n6) 0x52A9A0
/*cdecl*/ void CMessages::AddMessageSoonWithNumber(ushort *text,uint time,ushort flag, int n1, int n2, int n3, int n4, int n5, int n6) 0x52AAC0
/*cdecl*/ void CMessages::AddBigMessageWithNumber(ushort *text,uint time,ushort flag, int n1, int n2, int n3, int n4, int n5, int n6) 0x52AD10
/*cdecl*/ void CMessages::AddBigMessageWithNumberQ(ushort *text,uint time,ushort flag, int n1, int n2, int n3, int n4, int n5, int n6) 0x52AE00
/*cdecl*/ void CMessages::AddMessageWithString(ushort *text,uint time,ushort flag,ushort *str) 0x52AF30
/*cdecl*/ void CMessages::AddMessageJumpQWithString(ushort *text,uint time,ushort flag,ushort *str) 0x52B050
/*cdecl*/ void CMessages::ClearThisPrint(ushort *text) 0x52B140
/*cdecl*/ void CMessages::ClearThisBigPrint(ushort *text) 0x52B3C0
/*cdecl*/ void CMessages::ClearAllMessagesDisplayedByGame(void) 0x52B670
/*thiscall*/ void CMloModelInfo::CMloModelInfo(void) 0x50C100 
/*thiscall*/ void CMloModelInfo::~CMloModelInfo() 0x50C0E0 
/*cdecl*/ CClumpModelInfo* CModelInfo::AddClumpModel(int index) 0x50BA10
/*cdecl*/ CMloModelInfo* CModelInfo::AddMloModel(int index) 0x50B970
/*cdecl*/ CPedModelInfo* CModelInfo::AddPedModel(int index) 0x50BAD0
/*cdecl*/ CSimpleModelInfo* CModelInfo::AddSimpleModel(int index) 0x50B920
/*cdecl*/ CTimeModelInfo* CModelInfo::AddTimeModel(int index) 0x50B9C0
/*cdecl*/ CVehicleModelInfo* CModelInfo::AddVehicleModel(int index) 0x50BA60
/*cdecl*/ void CModelInfo::ConstructMloClumps(void) 0x50BB40 
/*cdecl*/ void* CModelInfo::Get2dEffectStore(void) 0x50BB30
/*cdecl*/ void* CModelInfo::GetMloInstanceStore(void) 0x50BB20
/*cdecl*/ CBaseModelInfo* CModelInfo::GetModelInfo(char const* name,int *index) 0x50B860
/*cdecl*/ void CModelInfo::Initialise(void) 0x50B310 
/*cdecl*/ bool CModelInfo::IsBoatModel(int index) 0x50BB90
/*cdecl*/ void CModelInfo::ReInit2dEffects(void) 0x50B580 
/*cdecl*/ void CModelInfo::RemoveColModelsFromOtherLevels(eLevelName) 0x50BBC0 
/*cdecl*/ void CModelInfo::ShutDown(void) 0x50B5B0 
/*thiscall*/ void CMouseControllerState::CMouseControllerState(void) 0x491B80 
/*thiscall*/ void CMouseControllerState::Clear(void) 0x491BB0 
/*thiscall*/ int CMousePointerStateHelper::GetMouseSetUp(void) 0x491BD0 
/*thiscall*/ void CObject::CObject(CDummyObject *dummyObject) 0x4BAD50
/*thiscall*/ void CObject::CObject(int,bool) 0x4BACE0 
/*thiscall*/ void CObject::CObject(void) 0x4BABD0 
/*thiscall*/ bool CObject::CanBeDeleted(void) 0x4BB010 
/*cdecl*/ void CObject::DeleteAllMissionObjects(void) 0x4BBE60 
/*cdecl*/ void CObject::DeleteAllTempObjects(void) 0x4BBDF0 
/*cdecl*/ void CObject::DeleteAllTempObjectsInArea(CVector point, float radius) 0x4BBED0
/*thiscall*/ void CObject::Init(void) 0x4BAEC0 
/*thiscall*/ void CObject::ObjectDamage(float damage) 0x4BB240
/*thiscall*/ void CObject::RefModelInfo(int modelIndex) 0x4BBD80
/*cdecl*/ void CObject::operator delete(void *data) 0x4BAEA0
/*cdecl*/ void* CObject::operator new(uint size) 0x4BAE70
/*cdecl*/ void* CObject::operator new(uint size,int) 0x4BAE80
/*cdecl*/ float FindPlayerHeading(void) 0x4A1220;
/*cdecl*/ CVector& FindPlayerCentreOfWorld_NoSniperShift(void) 0x4A11C0;
/*cdecl*/ CVector& FindPlayerCentreOfWorld(int playerId) 0x4A1170;
/*cdecl*/ CPed* FindPlayerPed(void) 0x4A1150;
/*cdecl*/ CTrain* FindPlayerTrain(void) 0x4A1120;
/*cdecl*/ CEntity* FindPlayerEntity(void) 0x4A10F0;
/*cdecl*/ CVehicle* FindPlayerVehicle(void) 0x4A10C0;
/*cdecl*/ CVector& FindPlayerSpeed(void) 0x4A1090;
/*cdecl*/ CVector& FindPlayerCoors(void) 0x4A1030;
/*cdecl*/ RwTexture* GetFirstTexture(RwTexDictionary *texDictionary) 0x5264E0
/*cdecl*/ RwObject* GetFirstObject(RwFrame *frame) 0x526460
/*cdecl*/ RpAtomic* GetFirstAtomic(RpClump *clump) 0x526420
/*cdecl*/ void SetAmbientColours(RwRGBAReal *colours) 0x526FA0
/*cdecl*/ void SetAmbientColoursForPedsCarsAndObjects(void) 0x526F80
/*cdecl*/ void SetAmbientColours(void) 0x526F60
/*cdecl*/ void ActivateDirectional(void) 0x526F50
/*cdecl*/ void DeActivateDirectional(void) 0x526F40
/*cdecl*/ void ReSetAmbientAndDirectionalColours(void) 0x526F10
/*cdecl*/ void SetBrightMarkerColours(float power) 0x526E60
/*cdecl*/ void SetAmbientAndDirectionalColours(float power) 0x526DE0
/*cdecl*/ void RemoveExtraDirectionalLights(RpWorld *world) 0x526DB0
/*cdecl*/ void AddAnExtraDirectionalLight(RpWorld *world,float x,float y,float z,float red,float green,float blue) 0x526C70
/*cdecl*/ void WorldReplaceNormalLightsWithScorched(RpWorld *world,float intensity) 0x526C10
/*cdecl*/ RpWorld* LightsDestroy(RpWorld *world) 0x526B40
/*cdecl*/ RpWorld* LightsCreate(RpWorld *world) 0x5269A0
/*cdecl*/ void SetLightsWithTimeOfDayColour(RpWorld *world) 0x526510
/*cdecl*/ RwFrame* GetFirstChild(RwFrame *frame) 0x5264A0
/*cdecl*/ RpAtomic* GetFirstAtomicCallback(RpAtomic *atomic, void *data) 0x526410
/*cdecl*/ RwObject* GetFirstObjectCallback(RwObject *object, void *data) 0x526450
/*cdecl*/ RwFrame* GetFirstFrameCallback(RwFrame *frame, void *data) 0x526490
/*cdecl*/ RwTexture* GetFirstTextureCallback(RwTexture *texture, void *data) 0x5264D0
/*cdecl*/ void WorldReplaceScorchedLightsWithNormal(RpWorld *world) 0x526C50
/*cdecl*/ void CreateDebugFont(void) 0x526300
/*cdecl*/ void DestroyDebugFont(void) 0x526310
/*cdecl*/ void FlushObrsPrintfs(void) 0x526320
/*cdecl*/ void DefinedState(void) 0x526330
/*cdecl*/ CAnimBlendClumpData* RpAnimBlendAllocateData(RpClump *clump) 0x4052A0
/*cdecl*/ bool RpAnimBlendPluginAttach() 0x4052D0
/*cdecl*/ AnimBlendFrameData* RpAnimBlendClumpFindFrame(RpClump *clump, char const *name) 0x405430
/*cdecl*/ void RpAnimBlendClumpInit(RpClump *clump) 0x405480
/*cdecl*/ bool RpAnimBlendClumpIsInitialized(RpClump *clump) 0x405500
/*cdecl*/ RpClump* AnimBlendClumpDestroy(RpClump *clump) 0x405240
/*thiscall*/ void CPad::AddToPCCheatString(char name) 0x492450 
/*thiscall*/ void CPad::CPad(void) 0x494EE0 
/*thiscall*/ bool CPad::CarGunJustDown(void) 0x4934F0
/*thiscall*/ bool CPad::ChangeStationJustDown(void) 0x493870
/*thiscall*/ void CPad::Clear(bool enable) 0x491A10 
/*thiscall*/ void CPad::ClearMouseHistory(void) 0x491B50 
/*thiscall*/ bool CPad::CycleCameraModeDownJustDown(void) 0x493830 
/*thiscall*/ bool CPad::CycleCameraModeUpJustDown(void) 0x4937D0 
/*thiscall*/ bool CPad::CycleWeaponLeftJustDown(void) 0x493910 
/*thiscall*/ bool CPad::CycleWeaponRightJustDown(void) 0x493940 
/*thiscall*/ void CPad::DoCheats(short) 0x492F20 
/*cdecl*/ void CPad::DoCheats(void) 0x492F00 
/*cdecl*/ void CPad::EditCodesForControls(int *) 0x494690 
/*cdecl*/ void CPad::EditString(char *name,int) 0x4944B0 
/*thiscall*/ bool CPad::ExitVehicleJustDown(void) 0x493650 
/*thiscall*/ bool CPad::ForceCameraBehindPlayer(void) 0x493D80 
/*thiscall*/ short CPad::GetAccelerate(void) 0x493780 
/*cdecl*/ bool CPad::GetAnaloguePadDown(void) 0x493BA0 
/*cdecl*/ bool CPad::GetAnaloguePadLeft(void) 0x493C00 
/*cdecl*/ bool CPad::GetAnaloguePadLeftJustUp(void) 0x493CC0 
/*cdecl*/ bool CPad::GetAnaloguePadRight(void) 0x493C60 
/*cdecl*/ bool CPad::GetAnaloguePadRightJustUp(void) 0x493D20 
/*cdecl*/ bool CPad::GetAnaloguePadUp(void) 0x493B40 
/*thiscall*/ short CPad::GetAnalogueUpDown(void) 0x493210
/*thiscall*/ short CPad::GetBrake(void) 0x4935A0
/*thiscall*/ bool CPad::GetCarGunFired(void) 0x493490
/*thiscall*/ short CPad::GetCarGunLeftRight(void) 0x4930C0
/*thiscall*/ short CPad::GetCarGunUpDown(void) 0x493070
/*thiscall*/ bool CPad::GetExitVehicle(void) 0x4935F0
/*thiscall*/ short CPad::GetHandBrake(void) 0x493560
/*thiscall*/ bool CPad::GetHorn(void) 0x493350
/*thiscall*/ bool CPad::GetLookBehindForCar(void) 0x4932F0 
/*thiscall*/ bool CPad::GetLookBehindForPed(void) 0x493320 
/*thiscall*/ bool CPad::GetLookLeft(void) 0x493290 
/*thiscall*/ bool CPad::GetLookRight(void) 0x4932C0 
/*cdecl*/ CPad* CPad::GetPad(int padNumber) 0x492F60
/*thiscall*/ short CPad::GetPedWalkLeftRight(void) 0x493110 
/*thiscall*/ short CPad::GetPedWalkUpDown(void) 0x493190 
/*thiscall*/ bool CPad::GetSprint(void) 0x493A70
/*thiscall*/ short CPad::GetSteeringLeftRight(void) 0x492F70 
/*thiscall*/ short CPad::GetSteeringUpDown(void) 0x492FF0 
/*thiscall*/ bool CPad::GetTarget(void) 0x493970
/*thiscall*/ int CPad::GetWeapon(void) 0x4936C0
/*thiscall*/ bool CPad::HornJustDown(void) 0x4933F0 
/*thiscall*/ bool CPad::JumpJustDown(void) 0x493A40 
/*thiscall*/ int CPad::LookAroundLeftRight(void) 0x493F80 
/*thiscall*/ int CPad::LookAroundUpDown(void) 0x494130 
/*cdecl*/ void CPad::PrintErrorMessage(void) 0x4942B0 
/*thiscall*/ void CPad::ProcessPCSpecificStuff(void) 0x492C60 
/*thiscall*/ void CPad::ReconcileTwoControllersInput(CControllerState const& controllerA,CControllerState const& controllerB) 0x491E60
/*thiscall*/ void CPad::ResetAverageWeapon(void) 0x494290
/*cdecl*/ void CPad::ResetCheats(void) 0x494450 
/*thiscall*/ bool CPad::ShiftTargetLeftJustDown(void) 0x493AE0 
/*thiscall*/ bool CPad::ShiftTargetRightJustDown(void) 0x493B10 
/*thiscall*/ short CPad::SniperModeLookLeftRight(void) 0x493EE0 
/*thiscall*/ short CPad::SniperModeLookUpDown(void) 0x493F30 
/*thiscall*/ bool CPad::SniperZoomIn(void) 0x493E00 
/*thiscall*/ bool CPad::SniperZoomOut(void) 0x493E70 
/*thiscall*/ void CPad::StartShake(short time,uchar frequency) 0x492230
/*thiscall*/ void CPad::StartShake_Distance(short time,uchar frequency,float x,float y,float z) 0x492290
/*thiscall*/ void CPad::StartShake_Train(float x,float y) 0x492360 
/*cdecl*/ void CPad::StopPadsShaking(void) 0x492F30 
/*thiscall*/ void CPad::StopShaking(short) 0x492F50 
/*thiscall*/ bool CPad::TargetJustDown(void) 0x4939D0
/*thiscall*/ void CPad::Update(void) 0x492C70 
/*thiscall*/ void CPad::UpdateMouse(void) 0x491CA0 
/*cdecl*/ void CPad::UpdatePads(void) 0x492720 
/*thiscall*/ void CPad::WeaponJustDown(void) 0x493700 
/*thiscall*/ void CPad::~CPad() 0x494ED0 
/*thiscall*/ void CPager::Init(void) 0x52B6F0
/*thiscall*/ void CPager::Process(void) 0x52B740
/*thiscall*/ void CPager::Display(void) 0x52B890
/*thiscall*/ void CPager::AddMessage(ushort *text,ushort,ushort,ushort) 0x52B940
/*thiscall*/ void CPager::AddMessageWithNumber(ushort *text,int n1,int n2,int n3,int n4,int n5,int n6,ushort,ushort,ushort) 0x52BB50
/*thiscall*/ void CPager::ClearMessages(void) 0x52BE00
/*thiscall*/ void CPager::RestartCurrentMessage(void) 0x52BE50 
/*cdecl*/ void CParticle::ReloadConfig(void) 0x50C430
/*cdecl*/ void CParticle::Initialise(void) 0x50C570
/*cdecl*/ void CParticle::Shutdown(void) 0x50CF40
/*cdecl*/ CParticle* CParticle::AddParticle(tParticleType type,CVector const&posn,CVector const&direction,CEntity *entity,float size,int rotationSpeed,int 
/*cdecl*/ CParticle* CParticle::AddParticle(tParticleType type,CVector const&posn,CVector const&direction,CEntity *entity,float,RwRGBA const&color,int 
/*cdecl*/ void CParticle::Update(void) 0x50DCF0
/*cdecl*/ void CParticle::Render(void) 0x50EE20
/*cdecl*/ void CParticle::RemovePSystem(tParticleType particleType) 0x50F6E0
/*cdecl*/ void CParticle::RemoveParticle(CParticle* particle,CParticle* previousParticle,tParticleSystemData *particleSystem) 0x50F720
/*cdecl*/ void CParticle::AddJetExplosion(CVector const& posn,float power,float size) 0x50F760
/*cdecl*/ void CParticle::AddYardieDoorSmoke(CVector const& posn,CMatrix const& matrix) 0x50FAA0
/*thiscall*/ void cParticleSystemMgr::cParticleSystemMgr(void) 0x50FCB0
/*thiscall*/ void cParticleSystemMgr::Initialise(void) 0x50FCD0
/*thiscall*/ void cParticleSystemMgr::LoadParticleData(void) 0x50FDF0
/*thiscall*/ void CPed::CPed(uint modelIndex) 0x4C41C0
/*thiscall*/ void CPedIK::CPedIK(void) 0x4ED010 
/*thiscall*/ void CPedIK::ExtractYawAndPitchLocal(RwMatrixTag *matrix,float &x,float &y) 0x4ED2C0
/*thiscall*/ void CPedIK::ExtractYawAndPitchWorld(RwMatrixTag *matrix,float &x,float &y) 0x4ED140
/*thiscall*/ void CPedIK::GetComponentPosition(RwV3d &pos,uint component) 0x4ED0F0
/*cdecl*/ RwMatrixTag* CPedIK::GetWorldMatrix(RwFrame *frame,RwMatrixTag *matrix) 0x4ED060
/*thiscall*/ bool CPedIK::LookAtPosition(CVector const& pos) 0x4ED590 
/*thiscall*/ bool CPedIK::LookInDirection(float x,float y) 0x4ED620 
/*thiscall*/ void CPedIK::MoveLimb(LimbOrientation &orient,float x,float y,LimbMovementInfo &info) 0x4ED440
/*thiscall*/ bool CPedIK::PointGunAtPosition(CVector const& pos) 0x4ED920 
/*thiscall*/ bool CPedIK::PointGunInDirection(float x,float y) 0x4ED9B0 
/*thiscall*/ bool CPedIK::PointGunInDirectionUsingArm(float x,float y) 0x4EDB20 
/*thiscall*/ bool CPedIK::RestoreGunPosn(void) 0x4EDD70 
/*thiscall*/ bool CPedIK::RestoreLookAt(void) 0x4ED810 
/*thiscall*/ void CPedIK::RotateTorso(AnimBlendFrameData *data,LimbOrientation &orient,bool) 0x4EDDB0
/*thiscall*/ void CPedModelInfo::CPedModelInfo(void) 0x50BFA0
/*thiscall*/ void CPedModelInfo::CreateHitColModel(void) 0x5104D0
/*thiscall*/ void CPedModelInfo::SetLowDetailClump(RpClump *clump) 0x510390
/*thiscall*/ void CPedModelInfo::~CPedModelInfo() 0x50BF60
/*cdecl*/ void CPedPlacement::FindZCoorForPed(CVector *position) 0x4EE340
/*cdecl*/ bool CPedPlacement::IsPositionClearForPed(CVector *position) 0x4EE2C0
/*cdecl*/ bool CPedPlacement::IsPositionClearOfCars(CVector *position) 0x4EE310
/*cdecl*/ uint CPedStats::GetPedStatType(char *pedStatName) 0x4EF780
/*cdecl*/ void CPedStats::Initialise(void) 0x4EF460 
/*cdecl*/ void CPedStats::LoadPedStats(void) 0x4EF580 
/*cdecl*/ void CPedStats::Shutdown(void) 0x4EF540 
/*cdecl*/ uint CPedType::FindPedFlag(char *flagName) 0x4EEF40
/*cdecl*/ uint CPedType::FindPedType(char *pedName) 0x4EEC10
/*cdecl*/ void CPedType::Initialise(void) 0x4EE7E0 
/*cdecl*/ void CPedType::Load(uchar *bufferPointer,uint structSize) 0x4EF3D0
/*cdecl*/ void CPedType::LoadPedData(void) 0x4EE8D0 
/*cdecl*/ void CPedType::Save(uchar *bufferPointer,uint *structSize) 0x4EF320
/*cdecl*/ void CPedType::Shutdown(void) 0x4EE890 
void CPhysical::ProcessEntityCollision(CEntity *entity, CColPoint *colPoint) 0x0
/*thiscall*/ void CPhysical::AddCollisionRecord(CEntity *entity) 0x497180
/*thiscall*/ void CPhysical::AddCollisionRecord_Treadable(CEntity *entity) 0x4970C0
/*thiscall*/ void CPhysical::AddToMovingList(void) 0x4958F0
/*thiscall*/ void CPhysical::ApplyAirResistance(void) 0x495C20
/*thiscall*/ bool CPhysical::ApplyCollision(CPhysical* phys, CColPoint &colPoint, float &, float &) 0x4973A0
/*thiscall*/ bool CPhysical::ApplyCollisionAlt(CEntity *entity, CColPoint &colPoint, float &, CVector &, CVector &) 0x4992A0
/*thiscall*/ bool CPhysical::ApplyFriction(CPhysical* phys, float, CColPoint &colPoint) 0x49A180
/*thiscall*/ bool CPhysical::ApplyFriction(float, CColPoint &colPoint) 0x499BE0
/*thiscall*/ void CPhysical::ApplyFriction(void) 0x495B80
/*thiscall*/ void CPhysical::ApplyFrictionMoveForce(float x, float y, float z) 0x495D90
/*thiscall*/ void CPhysical::ApplyFrictionTurnForce(float, float, float, float, float, float) 0x495E10
/*thiscall*/ void CPhysical::ApplyGravity(void) 0x495B50
/*thiscall*/ void CPhysical::ApplyMoveForce(float x, float y, float z) 0x4959A0
/*thiscall*/ void CPhysical::ApplyMoveSpeed(void) 0x495B10
/*thiscall*/ void CPhysical::ApplySpringCollisionAlt(float, CVector &, CVector &, float, float, CVector &) 0x499890
/*thiscall*/ void CPhysical::ApplySpringDampening(float, CVector &, CVector &, CVector &) 0x499990
/*thiscall*/ void CPhysical::ApplyTurnForce(float, float, float, float, float, float) 0x495A10
/*thiscall*/ void CPhysical::ApplyTurnSpeed(void) 0x497280
/*thiscall*/ bool CPhysical::CheckCollision(void) 0x496E50
/*thiscall*/ bool CPhysical::CheckCollision_SimpleCar(void) 0x496EB0
/*thiscall*/ bool CPhysical::GetHasCollidedWith(CEntity *entity) 0x497240
/*cdecl*/ void CPhysical::PlacePhysicalRelativeToOtherPhysical(CPhysical *phys1, CPhysical *phys2, CVector offset) 0x49F890
/*thiscall*/ bool CPhysical::ProcessCollisionSectorList(CPtrList *ptrList) 0x49B620
/*thiscall*/ bool CPhysical::ProcessCollisionSectorList_SimpleCar(CSector *sector) 0x49E790
/*thiscall*/ bool CPhysical::ProcessShiftSectorList(CPtrList *ptrList) 0x49DA10
/*thiscall*/ void CPhysical::RemoveAndAdd(void) 0x495540
/*thiscall*/ void CPhysical::RemoveFromMovingList(void) 0x495940
/*thiscall*/ void CPhysical::RemoveRefsToEntity(CEntity *entity) 0x49F820
/*thiscall*/ void CPlaceable::CPlaceable(void) 0x49F9A0
/*thiscall*/ bool CPlaceable::IsWithinArea(float x1,float y1,float z1,float x2,float y2,float z2) 0x49FAF0
/*thiscall*/ bool CPlaceable::IsWithinArea(float x1,float y1,float x2,float y2) 0x49FA50
/*thiscall*/ void CPlaceable::SetHeading(float heading) 0x49FA00
/*thiscall*/ void CPlaceable::~CPlaceable(void) 0x49F9E0
/*thiscall*/ void CPlaceName::CPlaceName(void) 0x4AD4B0 
/*thiscall*/ void CPlaceName::Display(void) 0x4AD5B0 
/*thiscall*/ void CPlaceName::Init(void) 0x4AD4C0 
/*thiscall*/ void CPlaceName::Process(void) 0x4AD4E0 
/*thiscall*/ void CPlane::CPlane(int modelIndex, uchar createdBy) 0x54B170
/*cdecl*/ void CPlane::CreateDropOffCesna(void) 0x54E160 
/*cdecl*/ void CPlane::FindDropOffCesnaCoordinates(void) 0x54E260 
/*cdecl*/ void CPlane::FindDrugPlaneCoordinates(void) 0x54E280 
/*cdecl*/ bool CPlane::HasCesnaBeenDestroyed(void) 0x54E150 
/*cdecl*/ bool CPlane::HasCesnaLanded(void) 0x54E140 
/*cdecl*/ bool CPlane::HasDropOffCesnaBeenShotDown(void) 0x54E250 
/*cdecl*/ void CPlane::InitPlanes(void) 0x54B820 
/*cdecl*/ void CPlane::LoadPath(char const*,int &,float &,bool) 0x54BD50 
/*cdecl*/ void CPlane::Shutdown(void) 0x54BCD0 
/*cdecl*/ bool CPlane::TestRocketCollision(CVector *) 0x54DE90 
/*cdecl*/ void CPlane::UpdatePlanes(void) 0x54BEC0 
/*cdecl*/ void CreateIncomingCesna(void) 0x54E000
/*thiscall*/ void CPlayerPed::AnnoyPlayerPed(bool) 0x4F3700 
/*thiscall*/ void CPlayerPed::CPlayerPed(void) 0x4EF7E0 
/*thiscall*/ void CPlayerPed::ClearAdrenaline(void) 0x4F3730 
/*thiscall*/ void CPlayerPed::ClearWeaponTarget(void) 0x4F28A0 
/*cdecl*/ void CPlayerPed::DeactivatePlayerPed(int playerId) 0x4EFC00
/*thiscall*/ void CPlayerPed::DoStuffToGoOnFire(void) 0x4F36E0 
/*thiscall*/ bool CPlayerPed::DoWeaponSmoothSpray(void) 0x4F1380 
/*thiscall*/ bool CPlayerPed::DoesTargetHaveToBeBroken(CVector,CWeapon *weapon) 0x4F3350
/*thiscall*/ void CPlayerPed::EvaluateNeighbouringTarget(CEntity *target,CEntity **outTarget,float *outTargetPriority,float maxDistance,float,bool) 0x4F2FA0
/*thiscall*/ void CPlayerPed::EvaluateTarget(CEntity *target, CEntity **outTarget, float *outTargetPriority, float maxDistance,float,bool) 0x4F2B60
/*thiscall*/ bool CPlayerPed::FindNextWeaponLockOnTarget(CEntity *target,bool) 0x4F2D50
/*thiscall*/ bool CPlayerPed::FindWeaponLockOnTarget(void) 0x4F28D0 
/*thiscall*/ CPlayerInfo* CPlayerPed::GetPlayerInfoForThisPlayerPed(void) 0x4F36C0
/*thiscall*/ bool CPlayerPed::IsThisPedAttackingPlayer(CPed *ped) 0x4F2D00 
/*thiscall*/ void CPlayerPed::KeepAreaAroundPlayerClear(void) 0x4F3460 
/*thiscall*/ void CPlayerPed::MakeChangesForNewWeapon(signed char weaponSlot) 0x4F2560
/*thiscall*/ void CPlayerPed::MakeObjectTargettable(int) 0x4F32B0 
/*thiscall*/ void CPlayerPed::PlayerControl1stPersonRunAround(CPad *pad) 0x4F1970 
/*thiscall*/ void CPlayerPed::PlayerControlFighter(CPad *pad) 0x4F1810 
/*thiscall*/ void CPlayerPed::PlayerControlM16(CPad *pad) 0x4F1DF0 
/*thiscall*/ void CPlayerPed::PlayerControlSniper(CPad *pad) 0x4F1CF0 
/*thiscall*/ void CPlayerPed::PlayerControlZelda(CPad *pad) 0x4F13C0 
/*thiscall*/ void CPlayerPed::ProcessAnimGroups(void) 0x4F2640 
/*thiscall*/ void CPlayerPed::ProcessPlayerWeapon(CPad *pad) 0x4F1EF0 
/*thiscall*/ void CPlayerPed::ProcessWeaponSwitch(CPad *pad) 0x4F2310 
/*thiscall*/ void CPlayerPed::ReApplyMoveAnims(void) 0x4F07C0 
/*cdecl*/ void CPlayerPed::ReactivatePlayerPed(int playerId) 0x4EFC20
/*thiscall*/ void CPlayerPed::RestoreSprintEnergy(float) 0x4F1340 
/*thiscall*/ void CPlayerPed::RunningLand(CPad *pad) 0x4F31D0 
/*thiscall*/ void CPlayerPed::SetInitialState(void) 0x4EFC40 
/*thiscall*/ void CPlayerPed::SetRealMoveAnim(void) 0x4F0880 
/*thiscall*/ void CPlayerPed::SetWantedLevel(int level) 0x4F3190
/*thiscall*/ void CPlayerPed::SetWantedLevelNoDrop(int level) 0x4F31B0
/*cdecl*/ void CPlayerPed::SetupPlayerPed(int playerId) 0x4EFB60
/*thiscall*/ void CPlayerPed::UseSprintEnergy(void) 0x4F12A0 
/*cdecl*/ void CPlayerSkin::BeginFrontendSkinEdit(void) 0x59BC70 
/*cdecl*/ void CPlayerSkin::EndFrontendSkinEdit(void) 0x59BCB0 
/*cdecl*/ RwTexture* CPlayerSkin::GetSkinTexture(char const* name) 0x59B9F0
/*cdecl*/ void CPlayerSkin::Initialise(void) 0x59B9B0 
/*cdecl*/ void CPools::Initialise(void) 0x4A1770
/*cdecl*/ void CPools::ShutDown(void) 0x4A1880
/*cdecl*/ void CPools::CheckPoolsEmpty(void) 0x4A1A50
/*cdecl*/ void CPools::GetPedRef(CPed *ped) 0x4A1A80
/*cdecl*/ CPed* CPools::GetPed(int handle) 0x4A1AA0
/*cdecl*/ CVehicle* CPools::GetVehicleRef(CVehicle *vehicle) 0x4A1AC0
/*cdecl*/ void CPools::GetVehicle(int handle) 0x4A1AE0
/*cdecl*/ void CPools::GetObjectRef(CObject *object) 0x4A1B00
/*cdecl*/ CObject* CPools::GetObject(int handle) 0x4A1B20
/*cdecl*/ void CPools::LoadVehiclePool(uchar *buffer,uint size) 0x4A1B40
/*cdecl*/ void CPools::SaveVehiclePool(uchar *buffer,uint *outSize) 0x4A2080
/*cdecl*/ void CPools::SaveObjectPool(uchar *buffer,uint *outSize) 0x4A22D0
/*cdecl*/ void CPools::LoadObjectPool(uchar *buffer,uint size) 0x4A2550
/*cdecl*/ void CPools::SavePedPool(uchar *buffer,uint *outSize) 0x4A29B0
/*cdecl*/ void CPools::LoadPedPool(uchar *buffer,uint size) 0x4A2B50
/*cdecl*/ void CPools::MakeSureSlotInObjectPoolIsEmpty(int slot) 0x4A2DB0
/*thiscall*/ void CProjectile::CProjectile(int modelIndex) 0x4BFE30
/*cdecl*/ void CPtrNode::operator delete(void *data) 0x4A3DE0
/*cdecl*/ void* CPtrNode::operator new(uint size) 0x4A3DD0
/*thiscall*/ void CPtrList::Flush(void) 0x4A3E00
/*thiscall*/ void CQuaternion::Get(RwMatrixTag *) 0x4BA0D0
/*thiscall*/ void CQuaternion::Slerp(CQuaternion const& from,CQuaternion const& to, float halftheta, float sintheta_inv, float t) 0x4BA1C0
/*cdecl*/ void CReferences::Init(void) 0x4A7350 
/*cdecl*/ void CReferences::PruneAllReferencesInWorld(void) 0x4A75A0 
/*cdecl*/ void CReferences::RemoveReferencesToPlayer(void) 0x4A7570 
/*thiscall*/ void CRGBA::CRGBA(uchar r, uchar g, uchar b, uchar a) 0x4F8C20
/*thiscall*/ void CRGBA::~CRGBA() 0x40B290
/*thiscall*/ void CRunningScript::Init(void) 0x4386C0
/*thiscall*/ char CRunningScript::ProcessOneCommand(void) 0x439500
void CSimpleModelInfo::DeleteRwObject(void) 0x5179B0
void CSimpleModelInfo::CreateInstance(void) 0x517B60
void CSimpleModelInfo::CreateInstance(RwMatrixTag *) 0x517AC0
void CSimpleModelInfo::GetRwObject(void) 0x4A9BA0
/*thiscall*/ void CSimpleModelInfo::CSimpleModelInfo(void) 0x50C150 
/*thiscall*/ void CSimpleModelInfo::FindRelatedModel(void) 0x517C00 
/*thiscall*/ RpAtomic* CSimpleModelInfo::GetAtomicFromDistance(float distance) 0x517A00
/*thiscall*/ float CSimpleModelInfo::GetLargestLodDistance(void) 0x517A60 
/*thiscall*/ float CSimpleModelInfo::GetNearDistance(void) 0x517A90 
/*thiscall*/ void CSimpleModelInfo::IncreaseAlpha(void) 0x517C60 
/*thiscall*/ void CSimpleModelInfo::Init(void) 0x517990 
/*thiscall*/ void CSimpleModelInfo::SetAtomic(int number,RpAtomic *atomic) 0x517950
/*thiscall*/ void CSimpleModelInfo::SetLodDistances(float * distance) 0x517AA0
/*thiscall*/ void CSimpleModelInfo::SetupBigBuilding(void) 0x517B90 
/*cdecl*/ void CSpecialParticleStuff::CreateFoamAroundObject(CMatrix *matrix,float x,float y,float z,int time) 0x51BC50 
/*cdecl*/ void CSpecialParticleStuff::StartBoatFoamAnimation(void) 0x51C030 
/*cdecl*/ void CSpecialParticleStuff::UpdateBoatFoamAnimation(CMatrix *matrix) 0x51C040 
/*cdecl*/ void CSprite2d::AddSpriteToBank(int,CRect const& posn,CRGBA const& color,float,float,float,float,float,float,float,float) 0x51EBC0 
/*thiscall*/ void CSprite2d::CSprite2d(void) 0x51E9E0 
/*thiscall*/ void CSprite2d::~CSprite2d() 0x51E9F0
/*thiscall*/ void CSprite2d::Delete(void) 0x51EA00 
/*thiscall*/ void CSprite2d::Draw(CRect const& posn,CRGBA const& color) 0x51ED50 
/*thiscall*/ void CSprite2d::Draw(CRect const& posn,CRGBA const& color1,CRGBA const& color2,CRGBA const& color3,CRGBA const& color4) 0x51EDF0 
/*thiscall*/ void CSprite2d::Draw(CRect const& posn,CRGBA const& color,float u1,float v1,float u2,float v2,float u3,float v3,float u4,float v4) 0x51ED90 
/*thiscall*/ void CSprite2d::Draw(float x,float y,float width,float height,CRGBA const& color) 0x51ECE0
/*thiscall*/ void CSprite2d::Draw(float x1,float y1,float x2,float y2,float x3,float y3,float x4,float y4,CRGBA const& color) 0x51EE40 
/*cdecl*/ void CSprite2d::DrawBank(int) 0x51EC50
/*cdecl*/ void CSprite2d::DrawRect(CRect const& posn,CRGBA const& color) 0x51F970 
/*cdecl*/ void CSprite2d::DrawRect(CRect const& posn,CRGBA const& color1,CRGBA const& color2,CRGBA const& color3,CRGBA const& color4) 0x51FA00 
/*cdecl*/ int CSprite2d::GetBank(int,RwTexture *texture) 0x51EB70
/*cdecl*/ void CSprite2d::InitPerFrame(void) 0x51EAE0 
/*thiscall*/ void CSprite2d::SetAddressing(RwTextureAddressMode modeUV) 0x51EAA0
/*cdecl*/ void CSprite2d::SetMaskVertices(int numVerts,float *posn) 0x51F490
/*cdecl*/ void CSprite2d::SetRecipNearClip(void) 0x51EA20 
/*thiscall*/ void CSprite2d::SetRenderState(void) 0x51F950 
/*thiscall*/ void CSprite2d::SetTexture(char *name) 0x51EA40 
/*thiscall*/ void CSprite2d::SetTexture(char *name,char *maskName) 0x51EA70
/*cdecl*/ void CSprite2d::SetVertices(CRect const& posn,CRGBA const& color1,CRGBA const& color2,CRGBA const& color3,CRGBA const& color4,float u1,float v1,float 
/*cdecl*/ void CSprite2d::SetVertices(CRect const& posn,CRGBA const& color1,CRGBA const& color2,CRGBA const& color3,CRGBA const& color4,uint numVerts) 0x51EE90
/*cdecl*/ void CSprite2d::SetVertices(RwIm2DVertex *vertices,CRect const& posn,CRGBA const& color1,CRGBA const& color2,CRGBA const& color3,CRGBA const& 
/*cdecl*/ void CSprite2d::SetVertices(float x1,float y1,float x2,float y2,float x3,float y3,float x4,float y4,CRGBA const& color1,CRGBA const& color2,CRGBA 
/*cdecl*/ void CSprite2d::SetVertices(int numVerts,float *posn,float *texCoors,CRGBA const& color) 0x51F3E0
/*cdecl*/ void CStats::AnotherCriminalCaught(void) 0x04AB050 
/*cdecl*/ void CStats::AnotherFireExtinguished(void) 0x04AB080 
/*cdecl*/ void CStats::AnotherKillFrenzyPassed(void) 0x04AB240 
/*cdecl*/ void CStats::AnotherLifeSavedWithAmbulance(void) 0x04AB040 
/*cdecl*/ void CStats::CheckPointReachedSuccessfully(void) 0x04AB270 
/*cdecl*/ void CStats::CheckPointReachedUnsuccessfully(void) 0x04AB290 
/*cdecl*/ int CStats::FindCriminalRatingNumber(void) 0x04AB2A0 
/*cdecl*/ wchar_t* CStats::FindCriminalRatingString(void) 0x04AB090
/*cdecl*/ void CStats::Init(void) 0x04AAC60 
/*cdecl*/ void CStats::LoadStats(uchar *bufferPointer,uint structSize) 0x04AB670
/*cdecl*/ void CStats::Register4x4MayhemTime(int time) 0x04AB020
/*cdecl*/ void CStats::Register4x4OneTime(int time) 0x04AAFC0
/*cdecl*/ void CStats::Register4x4ThreeTime(int time) 0x04AB000
/*cdecl*/ void CStats::Register4x4TwoTime(int time) 0x04AAFE0
/*cdecl*/ void CStats::RegisterElBurroTime(int time) 0x04AAFA0
/*cdecl*/ void CStats::RegisterFastestTime(int statID,int time) 0x04AAF50
/*cdecl*/ void CStats::RegisterHighestScore(int statID,int score) 0x04AAF80
/*cdecl*/ void CStats::RegisterLevelAmbulanceMission(int level) 0x04AB060
/*cdecl*/ void CStats::RegisterLongestFlightInDodo(int distance) 0x04AB200
/*cdecl*/ void CStats::RegisterTimeTakenDefuseMission(int time) 0x04AB220
/*cdecl*/ void CStats::SaveStats(uchar *bufferPointer,uint *structSize) 0x04AB3E0
/*cdecl*/ void CStats::SetTotalNumberKillFrenzies(int number) 0x04AB250
/*cdecl*/ void CStats::SetTotalNumberMissions(int number) 0x04AB260
/*thiscall*/ CAutomobile* CStoredCar::RestoreCar(void) 0x427690
/*thiscall*/ void CStoredCar::StoreCar(CVehicle *car) 0x4275C0 
/*cdecl*/ void CStoredCar::SetExtras(char first, char second) 0x427820
/*thiscall*/ CStreamingInfo* CStreamingInfo::AddToList(CStreamingInfo* listStart) 0x406380
/*thiscall*/ bool CStreamingInfo::GetCdPosnAndSize(uint &posn, uint &size) 0x4063E0
/*thiscall*/ int CStreamingInfo::GetCdSize(void) 0x4063D0
/*thiscall*/ CStreamingInfo* CStreamingInfo::RemoveFromList(void) 0x4063A0
/*thiscall*/ void CStreamingInfo::SetCdPosnAndSize(uint posn, uint size) 0x406410
/*thiscall*/ void CTheCarGenerators::CTheCarGenerators(void) 0x543350
/*cdecl*/ unsigned int CTheCarGenerators::CreateCarGenerator(float x,float y,float z,float angle,int modelId,short primaryColor,short secondaryColor,uchar 
/*cdecl*/ void CTheCarGenerators::Init(void) 0x543020 
/*cdecl*/ void CTheCarGenerators::LoadAllCarGenerators(uchar *bufferPointer,uint structSize) 0x5431E0
/*cdecl*/ void CTheCarGenerators::Process(void) 0x542F40 
/*cdecl*/ void CTheCarGenerators::SaveAllCarGenerators(uchar *bufferPointer,uint *structSize) 0x543050
/*cdecl*/ void CTimeCycle::Initialise(void) 0x4ABAE0 
/*cdecl*/ void CTimeCycle::Update(void) 0x4ABF40 
/*thiscall*/ void CTimeModelInfo::CTimeModelInfo(void) 0x50C0A0 
/*thiscall*/ void CTimeModelInfo::FindOtherTimeModel(void) 0x517C80 
/*thiscall*/ void CTimeModelInfo::~CTimeModelInfo(void) 0x50C080 
/*cdecl*/ void CTimer::EndUserPause(void) 0x4AD4A0
/*cdecl*/ void CTimer::StartUserPause(void) 0x4AD490
/*cdecl*/ void CTimer::Stop(void) 0x4AD480
/*cdecl*/ bool CTimer::GetIsSlowMotionActive(void) 0x4AD450
/*cdecl*/ uint CTimer::GetCurrentTimeInCycles(void) 0x4AD410
/*cdecl*/ uint CTimer::GetCyclesPerMillisecond(void) 0x4AD3F0
/*cdecl*/ void CTimer::Resume(void) 0x4AD370
/*cdecl*/ void CTimer::Suspend(void) 0x4AD310
/*cdecl*/ void CTimer::Update(void) 0x4ACF70
/*cdecl*/ void CTimer::Shutdown(void) 0x4ACF60
/*cdecl*/ void CTimer::Initialise(void) 0x4ACE60
/*thiscall*/ void CTrain::AddPassenger(CPed *passenger) 0x5504A0
/*thiscall*/ void CTrain::CTrain(int modelIndex, uchar createdBy) 0x54E2A0
/*cdecl*/ void CTrain::InitTrains(void) 0x54F000 
/*thiscall*/ void CTrain::OpenTrainDoor(float state) 0x550360
/*cdecl*/ void CTrain::ReadAndInterpretTrackFile(char *filename,CTrainNode **nodes,short *,int,float *,float *,float *,CTrainInterpolationLine *,bool) 0x54EAB0
/*cdecl*/ void CTrain::Shutdown(void) 0x54F360 
/*thiscall*/ void CTrain::TrainHitStuff(CPtrList &ptrList) 0x550300
/*cdecl*/ void CTrain::UpdateTrains(void) 0x54F3A0 
/*thiscall*/ void CTrainDoor::CTrainDoor(void) 0x54E430 
/*thiscall*/ bool CTrainDoor::IsClosed(void) 0x5460F0 
/*thiscall*/ bool CTrainDoor::IsFullyOpen(void) 0x546120 
/*thiscall*/ void CTrainDoor::Open(float angle) 0x546200
/*thiscall*/ void CTrainDoor::RetTranslationWhenClosed(void) 0x546180 
/*thiscall*/ void CTrainDoor::RetTranslationWhenOpen(void) 0x5461C0 
/*thiscall*/ float cTransmission::CalculateDriveAcceleration(float const& gasPedal,uchar & currrentGear,float &,float const&,bool) 0x5506B0
/*thiscall*/ void cTransmission::CalculateGearForSimpleCar(float velocity,uchar & currrentGear) 0x550A00
/*thiscall*/ void cTransmission::InitGearRatios(void) 0x550590 
/*thiscall*/ void cTransmission::cTransmission(void) 0x550580 
/*thiscall*/ void CTreadable::CTreadable(void) 0x4059F0
/*cdecl*/ void CTreadable::operator delete(void *data) 0x405A40
/*cdecl*/ void* CTreadable::operator new(uint size) 0x405A30
/*cdecl*/ void CTxdStore::Initialise(void) 0x527440
/*cdecl*/ void CTxdStore::Shutdown(void) 0x527470
/*cdecl*/ void CTxdStore::GameShutdown(void) 0x527490
/*cdecl*/ int CTxdStore::AddTxdSlot(char const*name) 0x5274E0
/*cdecl*/ void CTxdStore::RemoveTxdSlot(int id) 0x527520
/*cdecl*/ char* CTxdStore::GetTxdName(int id) 0x527590
/*cdecl*/ int CTxdStore::FindTxdSlot(char const*name) 0x5275D0
/*cdecl*/ bool CTxdStore::LoadTxd(int id,char const*name) 0x5276B0
/*cdecl*/ bool CTxdStore::LoadTxd(int id,RwStream *stream) 0x527700
/*cdecl*/ bool CTxdStore::StartLoadTxd(int id,RwStream *stream) 0x527770
/*cdecl*/ bool CTxdStore::FinishLoadTxd(int id,RwStream *stream) 0x5277E0
/*cdecl*/ void CTxdStore::Create(int id) 0x527830
/*cdecl*/ void CTxdStore::RemoveTxd(int id) 0x527870
/*cdecl*/ void CTxdStore::SetCurrentTxd(int id) 0x5278C0
/*cdecl*/ void CTxdStore::PushCurrentTxd(void) 0x527900
/*cdecl*/ void CTxdStore::PopCurrentTxd(void) 0x527910
/*cdecl*/ void CTxdStore::AddRef(int id) 0x527930
/*cdecl*/ void CTxdStore::RemoveRef(int id) 0x527970
/*cdecl*/ void CTxdStore::RemoveRefWithoutDelete(int id) 0x5279C0
/*cdecl*/ int CTxdStore::GetNumRefs(int id) 0x527A00
/*cdecl*/ void CUserDisplay::Init(void) 0x4AD660 
/*cdecl*/ void CUserDisplay::Process(void) 0x4AD690 
void CVehicle::ProcessControlInputs(uchar playerNum) 0x54B150
void CVehicle::GetComponentWorldPosition(int componentId, CVector &posnOut) 0x4E4650
bool CVehicle::IsComponentPresent(int componentId) 0x54B160
void CVehicle::SetComponentRotation(int componentId, CVector) 0x542620
void CVehicle::OpenDoor(int componentId, eDoors door, float doorOpenRatio) 0x542630
void CVehicle::ProcessOpenDoor(uint, uint, float) 0x4DEAE0
bool CVehicle::IsDoorReady(eDoors door) 0x4E03E0
bool CVehicle::IsDoorFullyOpen(eDoors door) 0x4DE4E0
bool CVehicle::IsDoorClosed(eDoors door) 0x542640
bool CVehicle::IsDoorMissing(eDoors door) 0x4DE4F0
void CVehicle::RemoveRefsToVehicle(CEntity *entity) 0x4B3D20
void CVehicle::BlowUpCar(CEntity *damager) 0x444B10
bool CVehicle::SetUpWheelColModel(CColModel *wheelCol) 0x542650
void CVehicle::BurstTyre(uchar tyreComponentId) 0x542660
bool CVehicle::IsRoomForPedToLeaveCar(uint, CVector *) 0x4C7330
float CVehicle::GetHeightAboveRoad(void) 0x417E60
void CVehicle::PlayCarHorn(void) 0x415AF0
/*thiscall*/ bool CVehicle::AddPassenger(CPed *passenger) 0x551D90
/*thiscall*/ bool CVehicle::AddPassenger(CPed *passenger, uchar seatNumber) 0x551E10
/*thiscall*/ bool CVehicle::CanBeDeleted(void) 0x5511B0
/*thiscall*/ bool CVehicle::CanPedEnterCar(void) 0x5522F0
/*thiscall*/ bool CVehicle::CanPedExitCar(bool) 0x5523C0
/*thiscall*/ bool CVehicle::CanPedOpenLocks(CPed const*ped) 0x5522A0
/*thiscall*/ bool CVehicle::CarHasRoof(void) 0x552B70
/*thiscall*/ void CVehicle::ChangeLawEnforcerState(uchar state) 0x552820
/*thiscall*/ void CVehicle::DoFixedMachineGuns(void) 0x564300
/*thiscall*/ void CVehicle::ExtinguishCarFire(void) 0x552AF0
/*thiscall*/ void CVehicle::FlyingControl(eFlightModel flightModel) 0x552BB0
/*thiscall*/ void CVehicle::InflictDamage(CEntity *damager, eWeaponType weapon, float intensity, CVector coords) 0x551950
/*thiscall*/ bool CVehicle::IsLawEnforcementVehicle(void) 0x552880
/*thiscall*/ bool CVehicle::IsOnItsSide(void) 0x552260
/*thiscall*/ bool CVehicle::IsSphereTouchingVehicle(float x, float y, float z, float radius) 0x552620
/*thiscall*/ bool CVehicle::IsUpsideDown(void) 0x552230
/*thiscall*/ bool CVehicle::IsVehicleNormal(void) 0x5527E0
/*thiscall*/ void CVehicle::ProcessCarAlarm(void) 0x5525A0
/*thiscall*/ void CVehicle::ProcessDelayedExplosion(void) 0x551C90
/*thiscall*/ void CVehicle::ProcessWheel(CVector &, CVector &, CVector &, CVector &, int, float, float, float, char, float *, tWheelState *, ushort) 0x5512E0
/*thiscall*/ float CVehicle::ProcessWheelRotation(tWheelState, CVector const&, CVector const&, float) 0x551280
/*thiscall*/ void CVehicle::RemoveDriver(void) 0x5520A0
/*thiscall*/ void CVehicle::RemovePassenger(CPed *passenger) 0x551EB0
/*thiscall*/ void CVehicle::SetDriver(CPed * driver) 0x551F20
/*thiscall*/ CPed* CVehicle::SetUpDriver(void) 0x5520C0
/*thiscall*/ CPed* CVehicle::SetupPassenger(int seatNumber) 0x552160
/*thiscall*/ char CVehicle::ShufflePassengersToMakeSpace(void) 0x5528A0
/*thiscall*/ bool CVehicle::UsesSiren(void) 0x552200
/*cdecl*/ void CVehicle::operator delete(void *data) 0x551150
/*cdecl*/ void* CVehicle::operator new(uint size) 0x551120
/*cdecl*/ void* CVehicle::operator new(uint size, int) 0x551130
/*thiscall*/ void CVehicleModelInfo::AvoidSameVehicleColour(uchar *prim,uchar *sec) 0x5210A0 
/*thiscall*/ void CVehicleModelInfo::CVehicleModelInfo(void) 0x51FB10 
/*thiscall*/ void CVehicleModelInfo::ChooseComponent(void) 0x520AB0 
/*thiscall*/ void CVehicleModelInfo::ChooseSecondComponent(void) 0x520BE0 
/*thiscall*/ void CVehicleModelInfo::ChooseVehicleColour(uchar &prim,uchar &sec) 0x520FD0 
/*cdecl*/ RwObject* CVehicleModelInfo::ClearAtomicFlagCB(RwObject *object,void *data) 0x520360
/*cdecl*/ RwFrame* CVehicleModelInfo::CollapseFramesCB(RwFrame *frame,void *data) 0x51FE10
/*cdecl*/ void CVehicleModelInfo::DeleteVehicleColourTextures(void) 0x521650
/*thiscall*/ int CVehicleModelInfo::FindEditableMaterialList(void) 0x520DE0 
/*cdecl*/ RpAtomic* CVehicleModelInfo::GetEditableMaterialListCB(RpAtomic *atomic,void *data) 0x520DC0
/*cdecl*/ RpMaterial* CVehicleModelInfo::GetEditableMaterialListCB(RpMaterial *material,void *data) 0x520D30
/*cdecl*/ int CVehicleModelInfo::GetMaximumNumberOfPassengersFromNumberOfDoors(int modelId) 0x5219D0
/*thiscall*/ void CVehicleModelInfo::GetWheelPosn(int wheel,CVector &outVec) 0x520840
/*cdecl*/ RpMaterial* CVehicleModelInfo::HasAlphaMaterialCB(RpMaterial *material,void *data) 0x51FEF0
/*cdecl*/ RpMaterial* CVehicleModelInfo::HasSpecularMaterialCB(RpMaterial *material,void *data) 0x521770
/*cdecl*/ RpAtomic* CVehicleModelInfo::HideAllComponentsAtomicCB(RpAtomic *atomic,void *data) 0x51FED0
/*cdecl*/ RpAtomic* CVehicleModelInfo::HideDamagedAtomicCB(RpAtomic *atomic,void *data) 0x51FE70
/*cdecl*/ void CVehicleModelInfo::LoadEnvironmentMaps(void) 0x521680
/*cdecl*/ void CVehicleModelInfo::LoadVehicleColours(void) 0x521260
/*cdecl*/ RpAtomic* CVehicleModelInfo::MoveObjectsCB(RwObject *object,void *data) 0x51FE50
/*thiscall*/ void CVehicleModelInfo::PreprocessHierarchy(void) 0x5204D0 
/*cdecl*/ RwObject* CVehicleModelInfo::SetAtomicFlagCB(RwObject *object,void *data) 0x520340
/*thiscall*/ void CVehicleModelInfo::SetAtomicRenderCallbacks(void) 0x5202C0 
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetAtomicRendererCB(RpAtomic *atomic,void *data) 0x51FF10
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetAtomicRendererCB_BigVehicle(RpAtomic *atomic,void *data) 0x520030
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetAtomicRendererCB_Boat(RpAtomic *atomic,void *data) 0x520120
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetAtomicRendererCB_Heli(RpAtomic *atomic,void *data) 0x520210
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetAtomicRendererCB_Train(RpAtomic *atomic,void *data) 0x520230
/*thiscall*/ void CVehicleModelInfo::SetEnvironmentMap(void) 0x521890 
/*cdecl*/ RpAtomic* CVehicleModelInfo::SetEnvironmentMapCB(RpAtomic *atomic,void *data) 0x521820
/*cdecl*/ RpMaterial* CVehicleModelInfo::SetEnvironmentMapCB(RpMaterial *material,void *data) 0x5217A0
/*thiscall*/ void CVehicleModelInfo::SetVehicleColour(uchar prim,uchar sec) 0x520E70 
/*thiscall*/ void CVehicleModelInfo::SetVehicleComponentFlags(RwFrame *component,uint flags) 0x5203C0
/*cdecl*/ void CVehicleModelInfo::ShutdownEnvironmentMaps(void) 0x521720
/*thiscall*/ void CVehicleModelInfo::~CVehicleModelInfo(void) 0x50BFF0 
/*thiscall*/ void CWeaponEffects::CWeaponEffects(void) 0x564C40
/*cdecl*/ void CWeaponEffects::ClearCrossHair(void) 0x564D60 
/*cdecl*/ void CWeaponEffects::Init(void) 0x564C60 
/*cdecl*/ void CWeaponEffects::MarkTarget(CVector pos,uchar red,uchar green,uchar blue,uchar alpha,float size) 0x564D00
/*cdecl*/ void CWeaponEffects::Render(void) 0x564D70 
/*cdecl*/ void CWeaponEffects::Shutdown(void) 0x564CF0 
/*thiscall*/ void CWeaponEffects::~CWeaponEffects() 0x564C50
/*thiscall*/ void CWeaponInfo::CWeaponInfo(void) 0x5654F0
/*cdecl*/ eWeaponFire CWeaponInfo::FindWeaponFireType(char *name) 0x5653E0
/*cdecl*/ eWeaponType CWeaponInfo::FindWeaponType(char *name) 0x5653B0
/*cdecl*/ CWeaponInfo* CWeaponInfo::GetWeaponInfo(eWeaponType weaponType) 0x564FD0
/*cdecl*/ void CWeaponInfo::Initialise(void) 0x564EA0 
/*cdecl*/ void CWeaponInfo::LoadWeaponData(void) 0x564FE0 
/*cdecl*/ void CWeaponInfo::Shutdown(void) 0x564FB0
/*thiscall*/ void CWeaponInfo::~CWeaponInfo() 0x5654E0
/*cdecl*/ void CWeather::Init(void) 0x522BA0
/*cdecl*/ void CWeather::Update(void) 0x522C10
/*cdecl*/ void CWeather::ForceWeather(short weatherType) 0x523170
/*cdecl*/ void CWeather::ForceWeatherNow(short weatherType) 0x523180
/*cdecl*/ void CWeather::ReleaseWeather(void) 0x5231A0
/*cdecl*/ void CWeather::AddRain(void) 0x5231B0
/*cdecl*/ void RenderOneRainStreak(CVector start,CVector end,int,bool,float) 0x5240E0
/*cdecl*/ void CWeather::RenderRainStreaks(void) 0x524550
/*cdecl*/ void CWeather::StoreWeatherState(void) 0x524B20
/*cdecl*/ void CWeather::RestoreWeatherState(void) 0x524B60
/*thiscall*/ void CXtraCompsModelInfo::CXtraCompsModelInfo(void) 0x50BF10
/*thiscall*/ void CXtraCompsModelInfo::~CXtraCompsModelInfo() 0x50BEF0
/*cdecl*/ char* GetFrameNodeName(RwFrame *frame) 0x527150
/*cdecl*/ bool NodeNamePluginAttach(void) 0x527100
/*cdecl*/ int NodeNameStreamGetSize(int) 0x5270D0
/*cdecl*/ RwStream* NodeNameStreamRead(RwStream *stream, int length, int object) 0x5270A0
/*cdecl*/ RwStream* NodeNameStreamWrite(RwStream *stream, int length, int object) 0x527070