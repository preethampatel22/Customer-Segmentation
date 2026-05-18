// ── Embedded data (generated from Python analysis) ──
const DATA={total_customers:200,num_clusters:5,silhouette_score:0.44,
elbow:{k:[2,3,4,5,6,7,8,9,10],wcss:[400,280,180,110,95,85,78,73,69],sil:[0.35,0.38,0.40,0.44,0.42,0.39,0.37,0.35,0.33]},
clusters:[
{id:0,label:"Premium Customers",emoji:"💎",desc:"High Income, High Spending",count:38,pct:19,avgAge:28,avgIncome:148000,avgSpend:88,avgPurch:30,male:16,female:22,color:"#818cf8"},
{id:1,label:"Budget Conscious",emoji:"📦",desc:"Low Income, Low Spending",count:42,pct:21,avgAge:50,avgIncome:28000,avgSpend:18,avgPurch:5,male:20,female:22,color:"#f472b6"},
{id:2,label:"Moderate Customers",emoji:"⚖️",desc:"Average Income & Spending",count:48,pct:24,avgAge:36,avgIncome:78000,avgSpend:52,avgPurch:16,male:25,female:23,color:"#34d399"},
{id:3,label:"Affluent & Careful",emoji:"💰",desc:"High Income, Low Spending",count:35,pct:17.5,avgAge:52,avgIncome:142000,avgSpend:24,avgPurch:7,male:19,female:16,color:"#fbbf24"},
{id:4,label:"Enthusiastic Shoppers",emoji:"🛒",desc:"Low Income, High Spending",count:37,pct:18.5,avgAge:22,avgIncome:35000,avgSpend:89,avgPurch:31,male:15,female:22,color:"#60a5fa"}
]};
// Generate scatter points from clusters
const SCATTER=[];
DATA.clusters.forEach(c=>{for(let i=0;i<c.count;i++){
const inc=c.avgIncome+(Math.random()-.5)*60000;
const sp=Math.min(100,Math.max(1,c.avgSpend+(Math.random()-.5)*30));
const age=Math.min(65,Math.max(18,c.avgAge+Math.floor((Math.random()-.5)*20)));
SCATTER.push({income:Math.round(inc),spending:Math.round(sp),age,cluster:c.id,gender:Math.random()>.5?'Male':'Female',id:SCATTER.length+1,purchases:Math.max(1,Math.round(c.avgPurch+(Math.random()-.5)*10))});
}});

const COLORS=DATA.clusters.map(c=>c.color);

// ── Particles ──
(function(){const el=document.getElementById('bgParticles');
for(let i=0;i<15;i++){const p=document.createElement('div');p.className='particle';
const s=Math.random()*200+50;p.style.cssText=`width:${s}px;height:${s}px;left:${Math.random()*100}%;top:${Math.random()*100}%;background:${COLORS[i%5]};animation-delay:${Math.random()*10}s;animation-duration:${15+Math.random()*15}s`;
el.appendChild(p);}})();

// ── KPI Animation ──
function animateValue(el,end,prefix='',suffix='',dur=1500){
let start=0;const step=end/60;const isFloat=String(end).includes('.');
const fn=()=>{start+=step;if(start>=end){el.textContent=prefix+(isFloat?end.toFixed(2):end.toLocaleString())+suffix;return;}
el.textContent=prefix+(isFloat?start.toFixed(2):Math.floor(start).toLocaleString())+suffix;requestAnimationFrame(fn);};fn();
}
animateValue(document.querySelector('#kpiCustomers .kpi-value'),DATA.total_customers);
animateValue(document.querySelector('#kpiClusters .kpi-value'),DATA.num_clusters);
animateValue(document.getElementById('silhouetteValue'),DATA.silhouette_score);
const avgInc=Math.round(SCATTER.reduce((a,b)=>a+b.income,0)/SCATTER.length);
animateValue(document.getElementById('avgIncomeValue'),avgInc,'₹');

// ── Canvas Helper ──
function getCtx(id){const c=document.getElementById(id);c.width=c.parentElement.clientWidth-48;
c.height=300;return{canvas:c,ctx:c.getContext('2d'),w:c.width,h:c.height};}

function drawAxis(ctx,w,h,pad,xLabel,yLabel,xMax,yMax,xTicks,yTicks){
ctx.strokeStyle='rgba(148,163,184,0.15)';ctx.lineWidth=1;ctx.fillStyle='#64748b';ctx.font='11px "Space Grotesk"';
ctx.beginPath();ctx.moveTo(pad,pad);ctx.lineTo(pad,h-pad);ctx.lineTo(w-pad,h-pad);ctx.stroke();
for(let i=0;i<=yTicks;i++){const y=pad+(h-2*pad)*(i/yTicks);const val=Math.round(yMax*(1-i/yTicks));
ctx.fillText(val.toLocaleString(),5,y+4);ctx.beginPath();ctx.moveTo(pad,y);ctx.lineTo(w-pad,y);ctx.strokeStyle='rgba(148,163,184,0.06)';ctx.stroke();ctx.strokeStyle='rgba(148,163,184,0.15)';}
for(let i=0;i<=xTicks;i++){const x=pad+(w-2*pad)*(i/xTicks);const val=Math.round(xMax*(i/xTicks));
ctx.fillText(val.toLocaleString(),x-15,h-pad+18);}
ctx.fillStyle='#94a3b8';ctx.font='12px "Space Grotesk"';ctx.fillText(xLabel,w/2-30,h-5);
ctx.save();ctx.translate(12,h/2+30);ctx.rotate(-Math.PI/2);ctx.fillText(yLabel,0,0);ctx.restore();
}

// ── Scatter Plot ──
let currentView='income-spending';
function drawScatter(view){
const{ctx,w,h}=getCtx('scatterChart');const c=document.getElementById('scatterChart');
c.height=420;const pad=55;ctx.clearRect(0,0,w,h+120);
let xKey,yKey,xLabel,yLabel,xMax,yMax;
if(view==='income-spending'){xKey='income';yKey='spending';xLabel='Annual Income (₹)';yLabel='Spending Score';xMax=220000;yMax=100;}
else if(view==='income-age'){xKey='income';yKey='age';xLabel='Annual Income (₹)';yLabel='Age';xMax=220000;yMax=70;}
else{xKey='spending';yKey='age';xLabel='Spending Score';yLabel='Age';xMax=100;yMax=70;}
drawAxis(ctx,w,420,pad,xLabel,yLabel,xMax,yMax,6,5);
SCATTER.forEach(p=>{const x=pad+(w-2*pad)*(p[xKey]/xMax);const y=420-pad-(420-2*pad)*(p[yKey]/yMax);
ctx.beginPath();ctx.arc(x,y,5,0,Math.PI*2);ctx.fillStyle=COLORS[p.cluster]+'cc';ctx.fill();
ctx.strokeStyle=COLORS[p.cluster];ctx.lineWidth=1.5;ctx.stroke();});
// Centroids
DATA.clusters.forEach(c=>{let cx,cy;
if(view==='income-spending'){cx=c.avgIncome;cy=c.avgSpend;}
else if(view==='income-age'){cx=c.avgIncome;cy=c.avgAge;}
else{cx=c.avgSpend;cy=c.avgAge;}
const x=pad+(w-2*pad)*(cx/xMax);const y=420-pad-(420-2*pad)*(cy/yMax);
ctx.beginPath();ctx.moveTo(x-8,y-8);ctx.lineTo(x+8,y-8);ctx.lineTo(x,y+8);ctx.closePath();
ctx.fillStyle='#fff';ctx.fill();ctx.strokeStyle='#000';ctx.lineWidth=2;ctx.stroke();});
// Legend
const leg=document.getElementById('scatterLegend');leg.innerHTML='';
DATA.clusters.forEach(c=>{leg.innerHTML+=`<div class="legend-item"><div class="legend-dot" style="background:${c.color}"></div>${c.emoji} ${c.label}</div>`;});
}
drawScatter('income-spending');
document.querySelectorAll('.control-btn').forEach(btn=>{btn.addEventListener('click',()=>{
document.querySelectorAll('.control-btn').forEach(b=>b.classList.remove('active'));btn.classList.add('active');
drawScatter(btn.dataset.view);});});

// ── Elbow Chart ──
(function(){const{ctx,w,h}=getCtx('elbowChart');const pad=55;
drawAxis(ctx,w,h,pad,'K (Clusters)','WCSS',10,450,8,5);
const pts=DATA.elbow.k.map((k,i)=>({x:pad+(w-2*pad)*(k/10),y:h-pad-(h-2*pad)*(DATA.elbow.wcss[i]/450)}));
ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);pts.forEach(p=>ctx.lineTo(p.x,p.y));
ctx.strokeStyle='#818cf8';ctx.lineWidth=2.5;ctx.stroke();
pts.forEach(p=>{ctx.beginPath();ctx.arc(p.x,p.y,5,0,Math.PI*2);ctx.fillStyle='#818cf8';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();});
// Mark elbow at K=5
const elbowPt=pts[3];ctx.beginPath();ctx.arc(elbowPt.x,elbowPt.y,12,0,Math.PI*2);ctx.strokeStyle='#f472b6';ctx.lineWidth=2;ctx.setLineDash([4,4]);ctx.stroke();ctx.setLineDash([]);
ctx.fillStyle='#f472b6';ctx.font='bold 11px "Space Grotesk"';ctx.fillText('Elbow (K=5)',elbowPt.x-25,elbowPt.y-18);
})();

// ── Silhouette Chart ──
(function(){const{ctx,w,h}=getCtx('silhouetteChart');const pad=55;
drawAxis(ctx,w,h,pad,'K (Clusters)','Score',10,0.5,8,5);
const pts=DATA.elbow.k.map((k,i)=>({x:pad+(w-2*pad)*(k/10),y:h-pad-(h-2*pad)*(DATA.elbow.sil[i]/0.5)}));
ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);pts.forEach(p=>ctx.lineTo(p.x,p.y));
ctx.strokeStyle='#34d399';ctx.lineWidth=2.5;ctx.stroke();
pts.forEach(p=>{ctx.beginPath();ctx.arc(p.x,p.y,5,0,Math.PI*2);ctx.fillStyle='#34d399';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();});
const best=pts[3];ctx.beginPath();ctx.arc(best.x,best.y,12,0,Math.PI*2);ctx.strokeStyle='#fbbf24';ctx.lineWidth=2;ctx.setLineDash([4,4]);ctx.stroke();ctx.setLineDash([]);
ctx.fillStyle='#fbbf24';ctx.font='bold 11px "Space Grotesk"';ctx.fillText('Best (K=5)',best.x-20,best.y-18);
})();

// ── Distribution Chart ──
(function(){const{ctx,w,h}=getCtx('distributionChart');const pad=55;
ctx.fillStyle='#64748b';ctx.font='11px "Space Grotesk"';
const bw=(w-2*pad)/(DATA.clusters.length*1.5);
DATA.clusters.forEach((c,i)=>{const x=pad+i*(bw*1.5)+bw*.25;const bh=(h-2*pad)*(c.count/60);const y=h-pad-bh;
const grd=ctx.createLinearGradient(x,y,x,h-pad);grd.addColorStop(0,c.color);grd.addColorStop(1,c.color+'44');
ctx.fillStyle=grd;ctx.beginPath();ctx.roundRect(x,y,bw,bh,6);ctx.fill();
ctx.fillStyle='#f1f5f9';ctx.font='bold 13px "Space Grotesk"';ctx.fillText(c.count,x+bw/2-8,y-8);
ctx.fillStyle='#94a3b8';ctx.font='11px "Space Grotesk"';ctx.fillText('C'+c.id,x+bw/2-6,h-pad+16);});
ctx.fillStyle='#94a3b8';ctx.font='12px "Space Grotesk"';ctx.fillText('Cluster',w/2-20,h-5);
})();

// ── Radar Chart ──
(function(){const{ctx,w,h}=getCtx('radarChart');const cx=w/2,cy=h/2-5,r=Math.min(w,h)/2-50;
const labels=['Income','Spending','Age','Purchases'];const n=labels.length;
const maxVals=[200000,100,65,37];
for(let ring=1;ring<=4;ring++){ctx.beginPath();const rr=r*(ring/4);
for(let i=0;i<=n;i++){const ang=Math.PI*2*(i/n)-Math.PI/2;const x=cx+rr*Math.cos(ang);const y=cy+rr*Math.sin(ang);
i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);}ctx.closePath();ctx.strokeStyle='rgba(148,163,184,0.12)';ctx.lineWidth=1;ctx.stroke();}
labels.forEach((l,i)=>{const ang=Math.PI*2*(i/n)-Math.PI/2;const x=cx+(r+18)*Math.cos(ang);const y=cy+(r+18)*Math.sin(ang);
ctx.fillStyle='#94a3b8';ctx.font='11px "Space Grotesk"';ctx.textAlign='center';ctx.fillText(l,x,y+4);});
DATA.clusters.forEach(c=>{const vals=[c.avgIncome/maxVals[0],c.avgSpend/maxVals[1],c.avgAge/maxVals[2],c.avgPurch/maxVals[3]];
ctx.beginPath();vals.forEach((v,i)=>{const ang=Math.PI*2*(i/n)-Math.PI/2;const x=cx+r*v*Math.cos(ang);const y=cy+r*v*Math.sin(ang);
i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);});ctx.closePath();ctx.fillStyle=c.color+'22';ctx.fill();ctx.strokeStyle=c.color;ctx.lineWidth=2;ctx.stroke();});
ctx.textAlign='start';
})();

// ── Cluster Cards ──
(function(){const el=document.getElementById('clusterCards');
DATA.clusters.forEach(c=>{const femPct=Math.round(c.female/(c.male+c.female)*100);
el.innerHTML+=`<div class="cluster-card" data-cluster="${c.id}">
<div class="cluster-card-header"><span class="cluster-badge" style="background:${c.color}22;color:${c.color}">Cluster ${c.id}</span><span class="cluster-count">${c.count} customers (${c.pct}%)</span></div>
<div class="cluster-label">${c.emoji} ${c.label}<br><small style="color:#64748b">${c.desc}</small></div>
<div class="cluster-stats">
<div class="cluster-stat"><div class="cluster-stat-value">₹${(c.avgIncome/1000).toFixed(0)}K</div><div class="cluster-stat-label">Avg Income</div></div>
<div class="cluster-stat"><div class="cluster-stat-value">${c.avgSpend}</div><div class="cluster-stat-label">Avg Spending</div></div>
<div class="cluster-stat"><div class="cluster-stat-value">${c.avgAge}</div><div class="cluster-stat-label">Avg Age</div></div>
<div class="cluster-stat"><div class="cluster-stat-value">${c.avgPurch}</div><div class="cluster-stat-label">Avg Purchases</div></div>
</div>
<div class="cluster-gender"><div class="gender-bar"><div class="gender-fill" style="width:${femPct}%"></div></div></div>
<div class="gender-labels"><span>♂ ${c.male}</span><span>♀ ${c.female}</span></div>
</div>`;});})();

// ── Data Table ──
const ROWS_PER_PAGE=15;let currentPage=1;let filteredData=[...SCATTER];
function renderTable(){
const tbody=document.getElementById('tableBody');tbody.innerHTML='';
const start=(currentPage-1)*ROWS_PER_PAGE;const pageData=filteredData.slice(start,start+ROWS_PER_PAGE);
pageData.forEach(r=>{tbody.innerHTML+=`<tr>
<td>#${r.id}</td><td>${r.age}</td><td>${r.gender}</td><td>₹${r.income.toLocaleString()}</td>
<td>${r.spending}</td><td>${r.purchases}</td>
<td><span class="cluster-tag" style="background:${COLORS[r.cluster]}22;color:${COLORS[r.cluster]}">C${r.cluster}</span></td></tr>`;});
const totalPages=Math.ceil(filteredData.length/ROWS_PER_PAGE);const pag=document.getElementById('tablePagination');pag.innerHTML='';
for(let i=1;i<=totalPages;i++){pag.innerHTML+=`<button class="page-btn ${i===currentPage?'active':''}" onclick="goPage(${i})">${i}</button>`;}
}
window.goPage=function(p){currentPage=p;renderTable();};
// Filter
const sel=document.getElementById('clusterFilter');DATA.clusters.forEach(c=>{sel.innerHTML+=`<option value="${c.id}">Cluster ${c.id}</option>`;});
sel.addEventListener('change',()=>{currentPage=1;filteredData=sel.value==='all'?[...SCATTER]:SCATTER.filter(r=>r.cluster==sel.value);renderTable();});
document.getElementById('searchInput').addEventListener('input',e=>{const q=e.target.value;currentPage=1;
filteredData=q?SCATTER.filter(r=>String(r.id).includes(q)):[...SCATTER];renderTable();});
renderTable();

// ── Nav ──
document.querySelectorAll('.nav-link').forEach(a=>{a.addEventListener('click',()=>{
document.querySelectorAll('.nav-link').forEach(l=>l.classList.remove('active'));a.classList.add('active');});});
