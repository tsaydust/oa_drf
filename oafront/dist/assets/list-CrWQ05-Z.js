import{h as U,_ as ee,u as ae,a as s,b as te,x as le,d as R,e as t,w as l,O as oe,f as ne,F as M,E as v,s as $,o as d,g as O,i as j,m as H,y as T,c as f,k as A,t as ue,j as re,l as S,r as i,q as se,z as de,A as ie}from"./index-Bry-NjLa.js";const Y={list:r=>U.get("/salary/records",r),detail:r=>U.get(`/salary/records/${r}`),create:r=>U.post("/salary/records",r),update:(r,x)=>U.put(`/salary/records/${r}`,x)},me=r=>(de("data-v-cc80945f"),r=r(),ie(),r),pe={class:"filter-container"},ce=me(()=>j("span",{class:"mx-2"},"-",-1)),ve={__name:"list",setup(r){ae();const x=s([]),_=s(1),y=s(10),D=s(0),b=s(!1),m=s(""),L=s([]),q=s([]),V=s(null),o=s({dateRange:[],minAmount:null,maxAmount:null,departmentId:null}),u=s({employee:"",amount:0,effective_date:""}),w={employee:[{required:!0,message:"请选择员工",trigger:"change"}],amount:[{required:!0,message:"请输入薪资金额",trigger:"blur"}],effective_date:[{required:!0,message:"请选择生效日期",trigger:"change"}]},k=async()=>{try{const n={page:_.value,limit:y.value};o.value.dateRange&&o.value.dateRange.length===2&&(n.start_date=o.value.dateRange[0],n.end_date=o.value.dateRange[1]),o.value.minAmount!==null&&(n.min_amount=o.value.minAmount),o.value.maxAmount!==null&&(n.max_amount=o.value.maxAmount),o.value.departmentId&&(n.department_id=o.value.departmentId);const a=await Y.list(n);x.value=a.results,D.value=a.count}catch{v.error("获取薪资列表失败")}},F=async()=>{try{const n=await $.getStaffList(1,1e3);L.value=n.results}catch{v.error("获取员工列表失败")}},z=async()=>{try{const n=await $.getAllDepartment();q.value=n.results}catch{v.error("获取部门列表失败")}},g=()=>{_.value=1,k()},Q=()=>{o.value={dateRange:[],minAmount:null,maxAmount:null,departmentId:null},g()},G=()=>{m.value="新增薪资记录",b.value=!0,F()},J=async(n,a="salary")=>{m.value=a==="salary"?"编辑薪资":"修改生效时间";try{const p=await Y.detail(n.id);u.value={id:p.id,employee:p.employee,amount:p.amount||0,effective_date:p.effective_date||""},a==="salary"?(w.amount=[{required:!0,message:"请输入薪资金额",trigger:"blur"}],w.effective_date=[]):(w.amount=[],w.effective_date=[{required:!0,message:"请选择生效日期",trigger:"change"}]),b.value=!0,F()}catch{v.error("获取薪资详情失败")}},K=()=>{V.value&&V.value.resetFields(),u.value={employee:"",amount:0,effective_date:""}},W=async()=>{V.value&&await V.value.validate(async n=>{if(n)try{u.value.id?(await Y.update(u.value.id,u.value),v.success("更新成功")):(await Y.create(u.value),v.success("创建成功")),b.value=!1,k()}catch(a){v.error(a.message||"操作失败")}})};return te(()=>{z(),k()}),(n,a)=>{const p=i("el-date-picker"),c=i("el-form-item"),I=i("el-input-number"),B=i("el-option"),E=i("el-select"),C=i("el-button"),N=i("el-form"),h=i("el-table-column"),X=i("el-table"),Z=i("el-card"),P=le("permission");return d(),R(M,null,[t(oe,{title:"薪资列表"},{footer:l(()=>[t(O,{page:_.value,"onUpdate:page":a[6]||(a[6]=e=>_.value=e),limit:y.value,"onUpdate:limit":a[7]||(a[7]=e=>y.value=e),total:D.value,onPagination:k},null,8,["page","limit","total"])]),default:l(()=>[t(Z,null,{default:l(()=>[j("div",pe,[t(N,{inline:!0,model:o.value,class:"demo-form-inline"},{default:l(()=>[t(c,{label:"生效日期"},{default:l(()=>[t(p,{modelValue:o.value.dateRange,"onUpdate:modelValue":a[0]||(a[0]=e=>o.value.dateRange=e),type:"daterange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期","value-format":"YYYY-MM-DD",onChange:g},null,8,["modelValue"])]),_:1}),t(c,{label:"薪资范围"},{default:l(()=>[t(I,{modelValue:o.value.minAmount,"onUpdate:modelValue":a[1]||(a[1]=e=>o.value.minAmount=e),min:0,precision:2,placeholder:"最小金额",onChange:g},null,8,["modelValue"]),ce,t(I,{modelValue:o.value.maxAmount,"onUpdate:modelValue":a[2]||(a[2]=e=>o.value.maxAmount=e),min:0,precision:2,placeholder:"最大金额",onChange:g},null,8,["modelValue"])]),_:1}),t(c,{label:"部门"},{default:l(()=>[t(E,{modelValue:o.value.departmentId,"onUpdate:modelValue":a[3]||(a[3]=e=>o.value.departmentId=e),placeholder:"选择部门",clearable:"",onChange:g,style:{width:"100px"}},{default:l(()=>[(d(!0),R(M,null,H(q.value,e=>(d(),f(B,{key:e.id,label:e.name,value:e.id},null,8,["label","value"]))),128))]),_:1},8,["modelValue"])]),_:1}),t(c,null,{default:l(()=>[T((d(),f(C,{type:"primary",onClick:G},{default:l(()=>[A("新增薪资记录")]),_:1})),[[P,n.manager]]),t(C,{type:"primary",onClick:g},{default:l(()=>[A("查询")]),_:1}),t(C,{onClick:Q},{default:l(()=>[A("重置")]),_:1})]),_:1})]),_:1},8,["model"])]),t(X,{data:x.value,style:{width:"100%"},"row-style":{height:"60px"},border:""},{default:l(()=>[t(h,{prop:"employee_name",label:"员工姓名"}),t(h,{prop:"amount",label:"薪资金额"},{default:l(e=>[A(ue(e.row.amount),1)]),_:1}),t(h,{prop:"effective_date",label:"生效日期"}),t(h,{prop:"created_by_name",label:"创建人"}),T((d(),f(h,{label:"操作",width:"200",fixed:"right",align:"center"},{default:l(e=>[t(C,{type:"primary",link:"",icon:re(se),onClick:fe=>J(e.row,"salary")},{default:l(()=>[A("编辑薪资")]),_:2},1032,["icon","onClick"])]),_:1})),[[P,n.manager]])]),_:1},8,["data"]),t(O,{page:_.value,"onUpdate:page":a[4]||(a[4]=e=>_.value=e),limit:y.value,"onUpdate:limit":a[5]||(a[5]=e=>y.value=e),total:D.value,onPagination:k},null,8,["page","limit","total"])]),_:1})]),_:1}),t(ne,{modelValue:b.value,"onUpdate:modelValue":a[11]||(a[11]=e=>b.value=e),title:m.value,width:"500",onCancel:K,onSubmit:W},{default:l(()=>[t(N,{ref_key:"formRef",ref:V,model:u.value,rules:w,"label-width":"100px"},{default:l(()=>[m.value==="新增薪资记录"?(d(),f(c,{key:0,label:"员工",prop:"employee"},{default:l(()=>[t(E,{modelValue:u.value.employee,"onUpdate:modelValue":a[8]||(a[8]=e=>u.value.employee=e),placeholder:"请选择员工"},{default:l(()=>[(d(!0),R(M,null,H(L.value,e=>(d(),f(B,{key:e.id,label:e.username,value:e.id},null,8,["label","value"]))),128))]),_:1},8,["modelValue"])]),_:1})):S("",!0),m.value==="编辑薪资"||m.value==="新增薪资记录"?(d(),f(c,{key:1,label:"薪资金额",prop:"amount"},{default:l(()=>[t(I,{modelValue:u.value.amount,"onUpdate:modelValue":a[9]||(a[9]=e=>u.value.amount=e),min:0,precision:2},null,8,["modelValue"])]),_:1})):S("",!0),m.value==="编辑薪资"||m.value==="修改生效时间"||m.value==="新增薪资记录"?(d(),f(c,{key:2,label:"生效日期",prop:"effective_date"},{default:l(()=>[t(p,{modelValue:u.value.effective_date,"onUpdate:modelValue":a[10]||(a[10]=e=>u.value.effective_date=e),type:"date",placeholder:"选择生效日期",format:"YYYY-MM-DD","value-format":"YYYY-MM-DD"},null,8,["modelValue"])]),_:1})):S("",!0)]),_:1},8,["model"])]),_:1},8,["modelValue","title"])],64)}}},ge=ee(ve,[["__scopeId","data-v-cc80945f"]]);export{ge as default};
