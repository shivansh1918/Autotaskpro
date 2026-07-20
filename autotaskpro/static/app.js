document.addEventListener('DOMContentLoaded', ()=>{
  const toggle = document.getElementById('darkToggle')
  if(toggle){toggle.addEventListener('click', ()=>{document.body.classList.toggle('dark');showToast('Toggled dark mode')})}
});

function showToast(msg){
  const t=document.getElementById('toast');
  if(!t) return; t.textContent=msg; t.style.display='block'; t.setAttribute('aria-hidden','false');
  setTimeout(()=>{t.style.display='none'; t.setAttribute('aria-hidden','true')},2500);
}
