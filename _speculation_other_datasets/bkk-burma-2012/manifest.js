// Combined dataset was split into per-trip segments (no flights). Redirecting
// to strongest segment. Available: bkk-burma-2012__seg1, bkk-burma-2012__seg2, bkk-burma-2012__seg3 …
(function() {
  var params = new URLSearchParams(location.search);
  params.set('dataset', 'bkk-burma-2012__seg2');
  location.replace(location.pathname + '?' + params.toString() + location.hash);
})();
