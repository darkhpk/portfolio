window.TurEco = (function(){
  function toggleSearchFields(){
    const typeEl = document.getElementById('id_search_type');
    if(!typeEl) return;
    const hotelFields = document.querySelectorAll('.js-hotel');
    const transportFields = document.querySelectorAll('.js-transport');

    function apply(){
      const isHotel = typeEl.value === 'hotel';
      hotelFields.forEach(el => el.style.display = isHotel ? '' : 'none');
      transportFields.forEach(el => el.style.display = !isHotel ? '' : 'none');
    }
    typeEl.addEventListener('change', apply);
    apply();
  }
  return { toggleSearchFields };
})();
