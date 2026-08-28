async function loadSummary(){
  const token=document.getElementById('token').value;
  const res=await fetch('/api/v1/dashboard/summary',{headers:{'X-Admin-Token':token}});
  if(!res.ok){alert('Admin authentication failed');return;}
  const d=await res.json();
  const vals=[d.estates,d.divisions,d.fields,d.crop_records,d.disease_events,d.ai_predictions];
  document.querySelectorAll('#cards strong').forEach((el,i)=>el.textContent=Number(vals[i]).toLocaleString());
  localStorage.setItem('plantationai_admin_token',token);
}
const saved=localStorage.getItem('plantationai_admin_token');if(saved){document.getElementById('token').value=saved;loadSummary();}
