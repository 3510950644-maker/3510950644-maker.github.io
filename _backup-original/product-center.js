/* 产品中心：产品数据 + 目录渲染 + 详情抽屉 + 中英文切换
 * 中英文切换的通用逻辑在 i18n.js；这里监听 px:langchange 事件重新渲染
 */
const 产品页 = [
  {id:'psu',group:'film',name:'PSU 薄膜',nameEn:'PSU Film',label:'原膜 / 01',labelEn:'Base film / 01',desc:'耐高温、高透明、尺寸稳定的高功能聚砜薄膜。',descEn:'High-temperature, highly transparent and dimensionally stable polysulfone film.',intro:'PSU 薄膜采用聚砜树脂，通过高温挤出流延工艺制作，兼具卓越的耐高温、机械强度、耐化学性、介电性能和高透明性。',introEn:'PSU film is made from polysulfone resin by high-temperature extrusion casting, combining outstanding heat resistance, mechanical strength, 化工 resistance, dielectric performance and high transparency.',color:'v-violet',features:['耐高温与尺寸稳定','高透明性与介电性能','可热成型与层压','适配灭菌环境'],featuresEn:['Heat resistance and dimensional stability','High transparency and dielectric performance','Thermoformable and laminable','Suitable for sterilization environments'],scenes:['医疗器械','电子绝缘','高性能层压','工业视窗'],scenesEn:['Medical devices','Electrical insulation','High-performance laminates','Industrial windows'],series:['PSU 标准薄膜','PSU 高透明系列'],seriesEn:['PSU standard film','PSU high-clarity series']},
  {id:'ptfe',group:'film',name:'PTFE 薄膜',nameEn:'PTFE Film',label:'原膜 / 02',labelEn:'Base film / 02',desc:'耐温、耐腐蚀、低摩擦的高性能氟塑料薄膜。',descEn:'High-performance fluoropolymer film with heat, 化工 and friction resistance.',intro:'PTFE 具有极低的表面能，拥有出色的耐化学性、耐热性、耐寒性、电绝缘性和非粘附性，被誉为“塑料王”。',introEn:'PTFE has an extremely low surface energy and offers excellent 化工 resistance, heat and cold resistance, electrical insulation and non-stick properties — known as the “king of plastics”.',color:'v-blue',features:['连续使用温度高','极低摩擦系数','优异电绝缘性','耐强酸强碱与溶剂'],featuresEn:['High continuous service temperature','Extremely low friction coefficient','Excellent electrical insulation','Resistant to strong acids, alkalis and solvents'],scenes:['复合材料脱模','电线电缆绝缘','化工防腐','航空航天'],scenesEn:['Composite release','Wire and cable insulation','Chemical anti-corrosion','Aerospace'],series:['VB-3 真空袋膜','MR1/MR2 超高温离型膜'],seriesEn:['VB-3 vacuum bagging film','MR1/MR2 ultra-high-temperature release film']},
  {id:'pfa',group:'film',name:'PFA 薄膜',nameEn:'PFA Film',label:'原膜 / 03',labelEn:'Base film / 03',desc:'高纯、耐高温、耐腐蚀的透明氟膜。',descEn:'High-purity, heat-resistant and corrosion-resistant transparent fluoropolymer film.',intro:'PFA 薄膜可热封、热成型、焊接、金属化或层压，提供优质的高温耐蠕变性能和低温韧度，可连续使用至 260°C。',introEn:'PFA film can be heat-sealed, thermoformed, welded, metallized or laminated. It offers excellent high-temperature creep resistance and low-temperature toughness, with continuous service up to 260°C.',color:'v-orange',features:['连续耐温至 260°C','极佳耐化学腐蚀性','优质电性能','低渗透率'],featuresEn:['Continuous service up to 260°C','Excellent 化工 resistance','Superior electrical properties','Low permeability'],scenes:['半导体洁净制程','石化防腐','食品医药','电子电器'],scenesEn:['Semiconductor clean processes','Petro化工 anti-corrosion','Food and pharmaceutical','Electronics and electrical'],series:['PFA MR 系列','PFA HP 超纯系列','PFA 焊接膜'],seriesEn:['PFA MR series','PFA HP ultra-pure series','PFA welding film']},
  {id:'fep',group:'film',name:'FEP 薄膜',nameEn:'FEP Film',label:'原膜 / 04',labelEn:'Base film / 04',desc:'耐热、耐化学腐蚀且可热焊接的透明薄膜。',descEn:'Transparent film that is heat-resistant, 化工ly resistant and heat-weldable.',intro:'FEP 薄膜由氟化乙烯丙烯共聚物制作，具备氟材料薄膜的优良性能，可热焊接、热成型并与多种材料复合。',introEn:'FEP film is made from fluorinated ethylene propylene copolymer. It shares the excellent properties of fluoropolymer films and can be heat-welded, thermoformed and laminated with various materials.',color:'v-green',features:['优良电气性能','高透光率','可热焊接成型','耐化学腐蚀'],featuresEn:['Excellent electrical properties','High light transmittance','Heat-weldable and formable','Chemical resistance'],scenes:['生物医药','电子制造','绝缘防腐','高温复合材料'],scenesEn:['Bio医药','Electronics manufacturing','Insulation and anti-corrosion','High-temperature composites'],series:['FEP 标准膜','FEP 离型膜'],seriesEn:['FEP standard film','FEP release film']},
  {id:'etfe',group:'film',name:'ETFE 薄膜',nameEn:'ETFE Film',label:'原膜 / 05',labelEn:'Base film / 05',desc:'轻质、耐候、自清洁的高强度氟膜。',descEn:'Lightweight, weather-resistant, self-cleaning high-strength fluoropolymer film.',intro:'ETFE 薄膜具备优异的耐候性、自清洁性、低介电损耗和机械强度，适用于汽车、新能源、建筑及农业等场景。',introEn:'ETFE film delivers outstanding weather resistance, self-cleaning performance, low dielectric loss and mechanical strength, making it suitable for automotive, new-energy, architectural and agricultural 应用行业页.',color:'v-orange',features:['耐候与自清洁','高透光性','低介电损耗','优异抗撕裂强度'],featuresEn:['Weather resistance and self-cleaning','High light transmittance','Low dielectric loss','Excellent tear strength'],scenes:['车窗防护','新能源电池封装','农业大棚','建筑膜结构'],scenesEn:['Automotive window protection','Battery encapsulation','Agricultural greenhouses','Architectural membrane structures'],series:['ETFE EC 系列','ETFE 建筑膜','FlexFlon 农膜'],seriesEn:['ETFE EC series','ETFE architectural film','FlexFlon agricultural film']},
  {id:'光伏df',group:'film',name:'PVDF 薄膜',nameEn:'PVDF Film',label:'原膜 / 06',labelEn:'Base film / 06',desc:'耐化学、耐候、压电性能优异的功能薄膜。',descEn:'Functional film with excellent 化工 resistance, weathering and piezoelectric performance.',intro:'PVDF 薄膜拥有优异的耐化学腐蚀、耐候性和电性能，可通过后续加工实现压电、阻燃和复合应用。',introEn:'PVDF film offers excellent 化工 resistance, weather resistance and electrical properties, and can be further processed for piezoelectric, flame-retardant and composite 应用行业页.',color:'v-blue',features:['耐候性好','耐化学腐蚀','压电性能优异','阻燃与电绝缘'],featuresEn:['Good weather resistance','Chemical resistance','Excellent piezoelectric performance','Flame retardant and insulating'],scenes:['传感器','电子电气','化工防腐','水处理设备'],scenesEn:['Sensors','Electronics and electrical','Chemical anti-corrosion','Water treatment equipment'],series:['PVDF 压电膜','PVDF 防腐膜'],seriesEn:['PVDF piezoelectric film','PVDF anti-corrosion film']},
  {id:'peek',group:'film',name:'PEEK 薄膜',nameEn:'PEEK Film',label:'原膜 / 07',labelEn:'Base film / 07',desc:'耐极端温度与高强度的特种工程塑料膜。',descEn:'Specialty engineering film for extreme temperatures and high strength.',intro:'PEEK 薄膜在高温、高压和化学腐蚀环境中仍保持良好的机械性能和尺寸稳定性，适合高端工业应用。',introEn:'PEEK film maintains good mechanical properties and dimensional stability in high-temperature, high-pressure and 化工ly aggressive environments — ideal for advanced industrial 应用行业页.',color:'v-violet',features:['耐高温与高强度','耐辐射与耐磨','尺寸稳定性好','耐多种化学介质'],featuresEn:['High temperature and strength','Radiation and wear resistance','Good dimensional stability','Resistant to many 化工 media'],scenes:['航空航天','汽车电子','医疗器械','高端装备'],scenesEn:['Aerospace','Automotive 电子','Medical devices','Advanced equipment'],series:['PEEK 标准膜','PEEK 绝缘膜'],seriesEn:['PEEK standard film','PEEK insulating film']},
  {id:'pctfe',group:'film',name:'PCTFE 薄膜',nameEn:'PCTFE Film',label:'原膜 / 08',labelEn:'Base film / 08',desc:'低吸湿、低渗透的高洁净氟塑料薄膜。',descEn:'Ultra-low moisture absorption, low-permeability and high-purity fluoropolymer film.',intro:'PCTFE 薄膜拥有极低的吸湿率和水蒸气渗透率，在低温与高洁净环境中保持可靠性能。',introEn:'PCTFE film has extremely low moisture absorption and water-vapour transmission rates, keeping reliable performance in low-temperature and high-purity environments.',color:'v-blue',features:['低吸湿率','低气体渗透率','低温韧性好','高洁净度'],featuresEn:['Low moisture absorption','Low gas permeability','Good low-temperature toughness','High cleanliness'],scenes:['航空航天','低温密封','医药包装','半导体设备'],scenesEn:['Aerospace','Cryogenic sealing','Pharmaceutical packaging','Semiconductor equipment'],series:['PCTFE 透明膜','PCTFE 高阻隔膜'],seriesEn:['PCTFE transparent film','PCTFE high-barrier film']},
  {id:'thv',group:'film',name:'THV 薄膜',nameEn:'THV Film',label:'原膜 / 09',labelEn:'Base film / 09',desc:'柔韧、透明且耐化学的氟聚合物薄膜。',descEn:'Flexible, transparent and 化工ly resistant fluoropolymer film.',intro:'THV 薄膜拥有良好的柔韧性、透明性和低温性能，可与其他基材进行热熔复合。',introEn:'THV film offers good flexibility, transparency and low-temperature performance, and can be hot-melt laminated with other substrates.',color:'v-green',features:['柔韧透明','低温性能好','可热熔复合','耐化学介质'],featuresEn:['Flexible and transparent','Good low-temperature performance','Hot-melt laminable','Chemical resistance'],scenes:['软管内衬','光学组件','化学防护','柔性电子'],scenesEn:['Hose lining','Optical components','Chemical protection','Flexible 电子'],series:['THV 标准膜','THV 复合膜'],seriesEn:['THV standard film','THV composite film']},
  {id:'ec',group:'tape',name:'EC 长效疏水透波膜',nameEn:'EC Film',label:'胶带 / 01',labelEn:'Tape / 01',desc:'兼具疏水、自清洁与透波性能的功能薄膜。',descEn:'Functional film combining long-lasting hydrophobicity, self-cleaning and wave transparency.',intro:'EC 系列面向户外通信与电子设备防护，提供稳定的疏水、防尘和透波解决方案。',introEn:'The EC series is designed for outdoor communication and electronic equipment protection, providing stable hydrophobic, dust-proof and wave-transparent solutions.',color:'v-blue',features:['长效疏水','高透波性能','耐候自清洁','可加工复合'],featuresEn:['Long-lasting hydrophobicity','High wave transparency','Weather-resistant and self-cleaning','Processable and laminable'],scenes:['通信设备','雷达罩','户外电子','汽车雷达'],scenesEn:['Communication equipment','Radomes','Outdoor 电子','Automotive radar'],series:['EC 标准系列','EC 高透波系列'],seriesEn:['EC standard series','EC high-transparency series']},
  {id:'etfetape',group:'tape',name:'ETFE 胶带',nameEn:'ETFE Tape',label:'胶带 / 02',labelEn:'Tape / 02',desc:'耐高温、耐老化的高性能氟塑料胶带。',descEn:'High-performance fluoropolymer tape with heat and ageing resistance.',intro:'ETFE 胶带以 ETFE 薄膜为基材，拥有良好的耐候、绝缘和耐化学性能，适合长期户外应用。',introEn:'ETFE tape uses ETFE film as the base material and offers good weather, insulation and 化工 resistance for long-term outdoor use.',color:'v-orange',features:['耐高温耐老化','电气绝缘性好','耐化学腐蚀','长期户外稳定'],featuresEn:['Heat and ageing resistance','Good electrical insulation','Chemical resistance','Long-term outdoor stability'],scenes:['线束包覆','电池绝缘','电子保护','户外工程'],scenesEn:['Wire harness wrapping','Battery insulation','Electronic protection','Outdoor engineering'],series:['ETFE 单面胶带','ETFE 双面胶带'],seriesEn:['ETFE single-sided tape','ETFE double-sided tape']},
  {id:'ptfetape',group:'tape',name:'PTFE 胶带',nameEn:'PTFE Tape',label:'胶带 / 03',labelEn:'Tape / 03',desc:'低摩擦、不粘、耐高温的工业胶带。',descEn:'Industrial tape with low friction, non-stick and high-temperature properties.',intro:'PTFE 胶带以高性能 PTFE 薄膜为基材，适用于高温密封、绝缘保护和低摩擦输送场景。',introEn:'PTFE tape uses high-performance PTFE film as the base material and suits high-temperature sealing, insulation protection and low-friction conveying 应用行业页.',color:'v-slate',features:['低摩擦不粘','耐高温','绝缘性优异','化学稳定'],featuresEn:['Low friction and non-stick','High temperature resistance','Excellent insulation','Chemically stable'],scenes:['热封设备','高温绝缘','输送带覆膜','机械密封'],scenesEn:['Heat sealing equipment','High-temperature insulation','Conveyor belting','Mechanical seals'],series:['PTFE 玻纤胶带','PTFE 单面胶带'],seriesEn:['PTFE glass-cloth tape','PTFE single-sided tape']},
  {id:'psatape',group:'tape',name:'压敏胶带',nameEn:'PSA Tape',label:'胶带 / 04',labelEn:'Tape / 04',desc:'稳定粘接与洁净剥离兼顾的功能胶带。',descEn:'Functional tape balancing reliable adhesion with clean removal.',intro:'压敏胶带可根据不同基材、温度和剥离要求进行定制，提供稳定粘接与洁净施工体验。',introEn:'Pressure-sensitive tapes can be customized for different substrates, temperatures and peel requirements, delivering reliable bonding and a clean application.',color:'v-slate',features:['稳定粘接','洁净剥离','可定制胶系','适配多种基材'],featuresEn:['Reliable adhesion','Clean removal','Custom adhesive systems','Compatible with many substrates'],scenes:['电子组装','标识保护','复合材料','工业粘接'],scenesEn:['Electronics assembly','Labeling and protection','Composites','Industrial bonding'],series:['高温压敏胶带','低残胶保护膜'],seriesEn:['High-temperature PSA tape','Low-residue protective film']},
  {id:'fp',group:'composite',name:'FP 复合膜',nameEn:'FP Composite Film',label:'复合膜 / 01',labelEn:'Composite film / 01',desc:'面向高温复合材料成型的功能复合膜。',descEn:'Functional composite film for high-temperature composite forming.',intro:'FP 复合膜以氟塑料薄膜为核心，结合多层复合结构，为高温成型、脱模和表面保护提供解决方案。',introEn:'FP composite film is built around a fluoropolymer core with a multi-layer structure, providing solutions for high-temperature forming, release and surface protection.',color:'v-violet',features:['高温尺寸稳定','低残胶脱模','多层结构可定制','表面保护可靠'],featuresEn:['High-temperature dimensional stability','Low-residue release','Customizable multi-layer structure','Reliable surface protection'],scenes:['航空复材','风电叶片','半导体封装','高端装备'],scenesEn:['Aviation composites','Wind turbine blades','Semiconductor packaging','Advanced equipment'],series:['FP 离型复合膜','FP 表面保护膜'],seriesEn:['FP release composite film','FP surface protection film']},
  {id:'ep',group:'composite',name:'EP 复合膜',nameEn:'EP Composite Film',label:'复合膜 / 02',labelEn:'Composite film / 02',desc:'兼具阻隔、耐候与机械性能的复合材料。',descEn:'Composite material combining barrier, weathering and mechanical performance.',intro:'EP 复合膜通过多层材料结构实现性能互补，可按客户的厚度、幅宽和表面要求定制。',introEn:'EP composite film uses a multi-layer structure to combine complementary properties, and can be customized by thickness, width and surface requirements.',color:'v-green',features:['阻隔性能优异','耐候耐老化','机械强度高','规格灵活定制'],featuresEn:['Excellent barrier performance','Weather and ageing resistance','High mechanical strength','Flexible specifications'],scenes:['新能源封装','建筑防护','电子绝缘','工业复合'],scenesEn:['New-energy encapsulation','Building protection','Electrical insulation','Industrial composites'],series:['EP 阻隔复合膜','EP 绝缘复合膜'],seriesEn:['EP barrier composite film','EP insulating composite film']}
];

/* 当前语言下的字段取值 */
const isEn = () => (typeof window.pxLang === 'function' ? window.pxLang() === 'en' : false);
const pick = (zh, en) => (isEn() ? en : zh);

const grid = document.querySelector('#catalogGrid');
const empty = document.querySelector('#emptyState');
const count = document.querySelector('#resultCount');
const searchInput = document.querySelector('#productSearch');
const drawer = document.querySelector('#detailDrawer');
const drawerTabContent = document.querySelector('#drawerTabContent');
let currentFilter = 'all';
let currentProduct = null;
let currentTab = 'features';

const productName = p => pick(p.name, p.nameEn);
const productLabel = p => pick(p.label, p.labelEn);
const productDesc = p => pick(p.desc, p.descEn);
const productIntro = p => pick(p.intro, p.introEn);
const tabList = (p, tab) => (isEn() ? p[tab + 'En'] : p[tab]) || [];

function cardHTML(p) {
  const name = productName(p);
  return `<article class="catalog-card" data-group="${p.group}" data-id="${p.id}"><div class="catalog-card-visual ${p.color}"><span>${name.split(' ')[0]}</span></div><div class="catalog-card-body"><small>${productLabel(p)}</small><h3>${name}</h3><p>${productDesc(p)}</p><span class="more">${pick('查看产品详情 ↗', 'View product details ↗')}</span></div></article>`;
}

function render() {
  const q = searchInput.value.trim().toLowerCase();
  let visible = 0;
  document.querySelectorAll('.catalog-card').forEach(card => {
    const p = 产品页.find(item => item.id === card.dataset.id);
    const hay = (isEn() ? p.nameEn + p.descEn : p.name + p.desc).toLowerCase();
    const ok = (currentFilter === 'all' || p.group === currentFilter) && hay.includes(q);
    card.hidden = !ok;
    if (ok) visible++;
  });
  count.textContent = visible;
  empty.style.display = visible ? 'none' : 'block';
}

function renderGrid() {
  grid.innerHTML = 产品页.map(cardHTML).join('');
  render();
}

/* 卡片点击（事件委托，重新渲染后无需重新绑定） */
grid.addEventListener('click', e => {
  const card = e.target.closest('.catalog-card');
  if (card) openProduct(产品页.find(p => p.id === card.dataset.id));
});

document.querySelectorAll('.filter-btn').forEach(btn => btn.addEventListener('click', () => {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  currentFilter = btn.dataset.filter;
  render();
}));
searchInput.addEventListener('input', render);

function renderDrawer() {
  if (!currentProduct) return;
  const p = currentProduct;
  document.querySelector('#drawerVisual').className = `drawer-visual ${p.color}`;
  document.querySelector('#drawerVisual').textContent = productName(p).split(' ')[0];
  document.querySelector('#drawerCategory').textContent = productLabel(p);
  document.querySelector('#drawerTitle').textContent = productName(p);
  document.querySelector('#drawerIntro').textContent = productIntro(p);
  showTab(currentTab);
}

function openProduct(p) {
  if (!p) return;
  currentProduct = p;
  currentTab = 'features';
  document.querySelectorAll('.drawer-tab').forEach(t => t.classList.remove('active'));
  document.querySelector('.drawer-tab[data-tab="features"]').classList.add('active');
  renderDrawer();
  drawer.classList.add('open');
  history.replaceState(null, '', `#${p.id}`);
}

function showTab(tab) {
  currentTab = tab;
  const list = tabList(currentProduct, tab);
  drawerTabContent.innerHTML = list.length ? `<ul>${list.map(x => `<li>${x}</li>`).join('')}</ul>` : '';
}

document.querySelectorAll('.drawer-tab').forEach(tab => tab.addEventListener('click', () => {
  document.querySelectorAll('.drawer-tab').forEach(t => t.classList.remove('active'));
  tab.classList.add('active');
  showTab(tab.dataset.tab);
}));
document.querySelector('.drawer-close').addEventListener('click', () => drawer.classList.remove('open'));
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') drawer.classList.remove('open');
});

/* 切换语言后重渲染目录与已打开的详情 */
document.addEventListener('px:langchange', () => {
  renderGrid();
  if (drawer.classList.contains('open')) renderDrawer();
});

const menuBtn = document.querySelector('.menu-btn');
if (menuBtn) menuBtn.addEventListener('click', () => document.querySelector('.nav').classList.toggle('mobile-open'));

renderGrid();
const hashProduct = 产品页.find(p => p.id === location.hash.slice(1));
if (hashProduct) openProduct(hashProduct);
