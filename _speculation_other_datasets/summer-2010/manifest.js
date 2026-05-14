// Combined dataset was split into per-trip segments (no flights). Redirecting
// to strongest segment. Available: summer-2010__seg1, summer-2010__seg2, summer-2010__seg3 …
(function() {
  var params = new URLSearchParams(location.search);
  params.set('dataset', 'summer-2010__seg1');
  location.replace(location.pathname + '?' + params.toString() + location.hash);
})();
