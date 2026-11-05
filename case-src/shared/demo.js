(function(){
  'use strict';
  var C=window.CASE_CONFIG||{};
  var $=function(s){return document.querySelector(s)};
  var state={};
  var colors=['#286f62','#a6614f','#3c6f8f','#bf7a20'];

  function rng(seed){var x=seed>>>0;return function(){x=(1664525*x+1013904223)>>>0;return x/4294967296}}
  function noise(rand){return (rand()+rand()+rand()+rand()-2)*0.85}
  function mean(a){return a.reduce(function(s,v){return s+v},0)/Math.max(1,a.length)}
  function sd(a){var m=mean(a);return Math.sqrt(mean(a.map(function(v){return Math.pow(v-m,2)})))||1e-6}
  function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
  function fmt(v,d){return Number(v).toFixed(d==null?1:d)}
  function metric(label,value,note,kind){return '<div class="metric '+(kind||'')+'"><small>'+label+'</small><strong>'+value+'</strong><span>'+note+'</span></div>'}
  function explain(a,b,c){$('#explain').innerHTML=[a,b,c].map(function(x){return '<div><b>'+x[0]+'</b><p>'+x[1]+'</p></div>'}).join('')}

  function makeControls(){
    $('#title').textContent=C.title||'案例演示'; $('#subtitle').textContent=C.subtitle||'';
    $('#controls').innerHTML=(C.controls||[]).map(function(c){
      state[c.id]=c.value;
      if(c.type==='select')return '<div class="field"><label for="'+c.id+'">'+c.label+'</label><select id="'+c.id+'">'+c.options.map(function(o){return '<option value="'+o.value+'"'+(o.value===c.value?' selected':'')+'>'+o.label+'</option>'}).join('')+'</select></div>';
      return '<div class="field"><label for="'+c.id+'">'+c.label+'<output id="'+c.id+'-out">'+c.value+(c.unit||'')+'</output></label><input id="'+c.id+'" type="range" min="'+c.min+'" max="'+c.max+'" step="'+c.step+'" value="'+c.value+'"></div>';
    }).join('');
    (C.controls||[]).forEach(function(c){var e=$('#'+c.id);e.addEventListener('input',function(){state[c.id]=c.type==='select'?e.value:Number(e.value);var o=$('#'+c.id+'-out');if(o)o.textContent=e.value+(c.unit||'');run()})});
    $('#run').addEventListener('click',run);
  }

  function lineChart(series,opt){
    opt=opt||{};var W=860,H=300,p={l:48,r:18,t:22,b:35};var all=[];series.forEach(function(s){all=all.concat(s.values)});
    var min=opt.min==null?Math.min.apply(null,all):opt.min,max=opt.max==null?Math.max.apply(null,all):opt.max;if(max===min)max=min+1;
    var n=Math.max.apply(null,series.map(function(s){return s.values.length}));
    function x(i){return p.l+i*(W-p.l-p.r)/Math.max(1,n-1)}function y(v){return p.t+(max-v)*(H-p.t-p.b)/(max-min)}
    var g='';for(var i=0;i<5;i++){var yy=p.t+i*(H-p.t-p.b)/4;var val=max-i*(max-min)/4;g+='<line class="grid" x1="'+p.l+'" x2="'+(W-p.r)+'" y1="'+yy+'" y2="'+yy+'"/><text class="tick" x="5" y="'+(yy+4)+'">'+fmt(val,1)+'</text>'}
    series.forEach(function(s,si){var pts=s.values.map(function(v,i){return x(i)+','+y(v)}).join(' ');g+='<polyline class="series" stroke="'+(s.color||colors[si])+'" points="'+pts+'"/>'});
    if(opt.threshold!=null)g+='<line class="threshold" x1="'+p.l+'" x2="'+(W-p.r)+'" y1="'+y(opt.threshold)+'" y2="'+y(opt.threshold)+'"/><text class="tick" x="'+(W-120)+'" y="'+(y(opt.threshold)-5)+'">阈值 '+fmt(opt.threshold,1)+'</text>';
    if(opt.event!=null)g+='<line class="event" x1="'+x(opt.event)+'" x2="'+x(opt.event)+'" y1="'+p.t+'" y2="'+(H-p.b)+'"/><text class="tick" x="'+(x(opt.event)+5)+'" y="'+(p.t+12)+'">事件起点</text>';
    g+='<line class="axis" x1="'+p.l+'" x2="'+p.l+'" y1="'+p.t+'" y2="'+(H-p.b)+'"/><line class="axis" x1="'+p.l+'" x2="'+(W-p.r)+'" y1="'+(H-p.b)+'" y2="'+(H-p.b)+'"/><text class="tick" x="'+(W/2-30)+'" y="294">时间 / 样本序号</text>';
    $('#chart').innerHTML='<svg viewBox="0 0 '+W+' '+H+'" aria-hidden="true">'+g+'</svg>';
    $('#legend').innerHTML=series.map(function(s,si){return '<span><i style="background:'+(s.color||colors[si])+'"></i>'+s.name+'</span>'}).join('')+(opt.threshold!=null?'<span><i style="background:#bf7a20"></i>报警阈值</span>':'');
  }

  function leak(){
    var rand=rng(125),n=120,event=60,leak=Number(state.leak),ns=Number(state.noise),k=state.confirm==='on'?3:1,thr=Number(state.threshold),inlet=[],outlet=[],res=[];
    for(var i=0;i<n;i++){var base=100+3*Math.sin(i/10)+noise(rand)*ns;var qout=base-(i>=event?leak:0)+noise(rand)*ns*.7;inlet.push(base);outlet.push(qout);res.push(base-qout)}
    var bm=mean(res.slice(0,45)),bs=sd(res.slice(0,45)),score=res.map(function(v){return Math.max(0,(v-bm)/bs)}),hit=-1,streak=0,falseAlarm=0;
    score.forEach(function(v,i){streak=v>thr?streak+1:0;if(streak>=k&&hit<0)hit=i-k+1;if(i<event&&v>thr)falseAlarm++});
    var delay=hit>=event?hit-event:null,status=hit<0?'未报警':hit<event?'提前误报':'已检测';
    $('#chart-title').textContent='进出口流量差与异常分数';lineChart([{name:'入口流量',values:inlet},{name:'出口流量',values:outlet},{name:'异常分数',values:score,color:'#3c6f8f'}],{event:event,threshold:thr});
    $('#metrics').innerHTML=metric('判定',status,'连续 '+k+' 点确认',hit>=event?'good':'alert')+metric('检测延迟',delay==null?'—':delay+' min','相对泄漏起点')+metric('事前越阈点',falseAlarm+' 个','不是正式报警次数')+metric('质量平衡残差',fmt(mean(res.slice(70)),1)+' m³/h','泄漏后均值');
    explain(['业务量','入口流量−出口流量是质量平衡残差；泄漏会让残差持续上升。'],['智能方法','用健康窗口标准化为异常分数，再要求连续越阈，避免单点噪声触发。'],['负向控制','关闭连续确认会更快，却可能增加事前误报；把泄漏调低可观察漏检边界。']);
  }

  function corrosion(){
    var rand=rng(225),depth=Number(state.depth),ns=Number(state.noise),full=state.features==='full',cells=[],risks=[];
    for(var i=0;i<32;i++){var moisture=.25+.65*((i%8)/7),age=.2+.7*(Math.floor(i/8)/3),pit=clamp(depth+10*Math.sin(i*.9)+noise(rand)*ns,3,82);var z=full?(-4.6+.065*pit+1.25*moisture+1.05*age):(-3.7+.056*pit);var risk=1/(1+Math.exp(-z));risks.push(risk);cells.push({pit:pit,risk:risk})}
    var high=risks.filter(function(v){return v>=.65}).length,max=Math.max.apply(null,risks),idx=risks.indexOf(max),remaining=clamp(100-cells[idx].pit,5,98);
    $('#chart-title').textContent='管段腐蚀风险矩阵（32 个检测单元）';$('#legend').innerHTML='<span>浅色：低风险</span><span>深红：高风险</span>';
    $('#chart').innerHTML='<div class="matrix">'+cells.map(function(c,i){var r=Math.round(238-90*c.risk),g=Math.round(188-125*c.risk),b=Math.round(120-75*c.risk);return '<div class="cell" title="单元 '+(i+1)+'；壁厚损失 '+fmt(c.pit,0)+'%；风险 '+fmt(c.risk*100,0)+'%" style="background:rgb('+r+','+g+','+b+')">'+fmt(c.risk*100,0)+'%</div>'}).join('')+'</div><div class="warnline">颜色是教学风险分数，不替代腐蚀工程规范中的剩余强度评价、复检和专家签字。</div>';
    $('#metrics').innerHTML=metric('高风险单元',high+' / 32','阈值 65%',high?'alert':'good')+metric('最高风险',fmt(max*100,0)+'%','单元 '+(idx+1))+metric('剩余壁厚代理',fmt(remaining,0)+'%','100%−最大壁厚损失')+metric('特征路径',full?'多源融合':'仅壁厚','反事实开关');
    explain(['业务量','内检测得到壁厚损失；环境湿度与服役年限影响腐蚀发展的先验风险。'],['智能方法','逻辑风险模型融合多源特征，给每个管段排序，帮助安排复检优先级。'],['负向控制','切换为“仅壁厚”会让上下文信息失效，用来检验多源特征是否真正影响结果。']);
  }

  function network(){
    var target=Number(state.target),limit=Number(state.pressure),constraint=state.constraint==='on',price=Number(state.price),cand=[];
    for(var s=.72;s<=1.101;s+=.02)for(var v=.5;v<=1.001;v+=.025){var flow=132*s*Math.sqrt(v);var pressure=1.5+2.3*s*s/v;var energy=58*Math.pow(s,3)+18*Math.pow(1-v,2);var feasible=flow>=target&&pressure<=limit;var objective=energy*price+(constraint?(Math.max(0,target-flow)*8+(!feasible?10000:0)):0);cand.push({s:s,v:v,flow:flow,pressure:pressure,energy:energy,feasible:feasible,obj:objective})}
    cand.sort(function(a,b){return a.obj-b.obj});var best=cand[0],base=cand.reduce(function(p,c){return Math.abs(c.s-.98)+Math.abs(c.v-.9)<Math.abs(p.s-.98)+Math.abs(p.v-.9)?c:p},cand[0]);var save=(base.energy-best.energy)/base.energy*100;
    $('#chart-title').textContent='井组—汇管—泵站工况与优化解';$('#legend').innerHTML='<span><i style="background:#286f62"></i>流量路径</span><span><i style="background:#a6614f"></i>压力约束</span>';
    $('#chart').innerHTML='<svg class="network" viewBox="0 0 860 300"><defs><marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#286f62"/></marker></defs><g fill="none" stroke="#286f62" stroke-width="5" marker-end="url(#ar)"><path d="M115 70C250 70 250 145 385 145"/><path d="M115 145H385"/><path d="M115 220C250 220 250 145 385 145"/><path d="M465 145H695"/></g><g fill="#fff" stroke="#286f62" stroke-width="2"><circle cx="90" cy="70" r="27"/><circle cx="90" cy="145" r="27"/><circle cx="90" cy="220" r="27"/><rect x="385" y="110" width="80" height="70" rx="7"/><rect x="695" y="110" width="110" height="70" rx="7"/></g><g fill="#23302f" font-size="13" text-anchor="middle"><text x="90" y="75">井 1</text><text x="90" y="150">井 2</text><text x="90" y="225">井 3</text><text x="425" y="140">汇管</text><text x="425" y="158">阀 '+fmt(best.v*100,0)+'%</text><text x="750" y="138">泵站</text><text x="750" y="157">转速 '+fmt(best.s*100,0)+'%</text></g><g fill="#66716f" font-size="12"><text x="510" y="120">流量 '+fmt(best.flow,1)+' m³/h</text><text x="510" y="174">压力 '+fmt(best.pressure,2)+' MPa</text></g></svg>'+(best.feasible?'':'<div class="warnline">当前最优解违反产量或压力约束。这正是关闭约束后必须显式暴露的不可执行结果。</div>');
    $('#metrics').innerHTML=metric('推荐泵速',fmt(best.s*100,0)+'%','额定转速')+metric('推荐阀位',fmt(best.v*100,0)+'%','开度')+metric('预测能耗',fmt(best.energy,1)+' kWh','教学代理值')+metric('可执行性',best.feasible?'满足约束':'不可执行','流量与压力同时检查',best.feasible?'good':'alert');
    explain(['业务量','井口流量汇入集输管网；泵速、阀位共同改变输量、压力与能耗。'],['智能方法','对候选泵速和阀位做网格搜索，用能耗目标与工艺约束筛选推荐工况。'],['负向控制','关闭压力约束可能得到更省电但不可执行的方案，证明“优化”不能只看目标函数。']);
  }

  function meter(){
    var rand=rng(425),gf=Number(state.gas),drift=Number(state.drift)/100,enabled=state.correction==='on',rawErr=[],corrErr=[],raw=[],corr=[];
    for(var i=0;i<70;i++){var trueQ=80+9*Math.sin(i/8),temp=20+8*Math.sin(i/15),g=clamp(gf+.08*Math.sin(i/11),.05,.98);var bias=.085*g-.0012*(temp-25)+drift;var r=trueQ*(1+bias)+noise(rand)*.7;var c=enabled?r/(1+.085*g-.0012*(temp-25)+drift*.85):r;raw.push(r);corr.push(c);rawErr.push(Math.abs(r-trueQ)/trueQ*100);corrErr.push(Math.abs(c-trueQ)/trueQ*100)}
    var rawMape=mean(rawErr),corrMape=mean(corrErr),ood=gf>.82;
    $('#chart-title').textContent='原始计量与智能校正结果';lineChart([{name:'原始读数',values:raw},{name:'校正读数',values:corr},{name:'参考真值',values:raw.map(function(_,i){return 80+9*Math.sin(i/8)}),color:'#3c6f8f'}],{});
    $('#metrics').innerHTML=metric('原始 MAPE',fmt(rawMape,2)+'%','相对参考真值')+metric('校正后 MAPE',fmt(corrMape,2)+'%','当前 70 个样本',enabled?'good':'alert')+metric('误差改善',fmt(rawMape-corrMape,2)+' pct','百分点')+metric('适用域',ood?'超出训练域':'训练域内',ood?'含气率 > 82%':'含气率 ≤ 82%',ood?'alert':'good');
    explain(['业务量','多相流计量会受含气率、温度与仪表漂移共同影响，原始读数出现系统偏差。'],['智能方法','用运行特征估计系统偏差，再对原始读数做动态校正，并报告校正前后误差。'],['负向控制','关闭校正可观察原始误差；含气率超过训练范围时仍显示数值，但必须标记域外。']);
  }

  function tank(){
    var rand=rng(525),leak=Number(state.leak),ns=Number(state.noise),thermal=state.thermal==='on',n=100,event=45,level=[70],res=[],temp=[],score=[];
    for(var i=1;i<n;i++){var inflow=1.5+.3*Math.sin(i/9),outflow=1.4+.25*Math.cos(i/11),loss=i>=event?leak:0;var expected=(inflow-outflow)*.08;var observed=expected-loss*.09+noise(rand)*ns*.05;level.push(level[i-1]+observed);res.push(Math.max(0,expected-observed));temp.push(Math.max(0,(i>=event?leak*.8:0)+noise(rand)*ns*.25));score.push(res[res.length-1]*7+(thermal?temp[temp.length-1]:0))}
    var thr=2.4,hit=-1,streak=0,scoreEvent=event-1;score.forEach(function(v,i){streak=v>thr?streak+1:0;if(streak>=3&&hit<0)hit=i-2});var delay=hit>=scoreEvent?hit-scoreEvent:null;var drop=level[0]-level[level.length-1];
    $('#chart-title').textContent='液位质量平衡与热异常融合';lineChart([{name:'液位',values:level},{name:'融合异常分数',values:[0].concat(score),color:'#a6614f'}],{event:event,threshold:thr});
    $('#metrics').innerHTML=metric('报警状态',hit>=scoreEvent?'已检测':hit<0?'未报警':'提前误报','连续 3 点确认',hit>=scoreEvent?'good':'alert')+metric('检测延迟',delay==null?'—':delay+' min','相对泄漏起点')+metric('累计液位变化',fmt(drop,2)+' cm','期初−期末')+metric('热成像通道',thermal?'已融合':'已屏蔽','反事实开关');
    explain(['业务量','进出量决定理论液位变化；实测液位额外下降形成质量平衡残差。'],['智能方法','把液位残差与罐周热异常融合，连续越阈后报警，降低单传感器歧义。'],['负向控制','关闭热通道可检验多模态输入是否真正被消费；小泄漏和高噪声展示检测边界。']);
  }

  function run(){({leak:leak,corrosion:corrosion,network:network,meter:meter,tank:tank}[C.mode]||leak)()}
  makeControls();run();
})();
