/**
 * KrushiSarathi — cities per state/UT + generated demo labs (2–3 per city).
 * Lab names/contacts are deterministic (same city → same listings each load).
 */
(function () {
  'use strict';

  window.CITIES_BY_STATE = {
    'Andaman and Nicobar Islands': ['Port Blair', 'Car Nicobar', 'Havelock'],
    'Andhra Pradesh': ['Vijayawada', 'Visakhapatnam', 'Guntur', 'Tirupati'],
    'Arunachal Pradesh': ['Itanagar', 'Tawang', 'Pasighat'],
    'Assam': ['Guwahati', 'Dibrugarh', 'Silchar', 'Jorhat'],
    'Bihar': ['Patna', 'Gaya', 'Muzaffarpur', 'Bhagalpur'],
    'Chandigarh': ['Chandigarh'],
    'Chhattisgarh': ['Raipur', 'Bilaspur', 'Durg', 'Korba'],
    'Dadra and Nagar Haveli and Daman and Diu': ['Silvassa', 'Daman', 'Diu'],
    'Delhi': ['New Delhi', 'Dwarka', 'Rohini'],
    'Goa': ['Panaji', 'Margao', 'Vasco da Gama'],
    'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar'],
    'Haryana': ['Gurugram', 'Faridabad', 'Karnal', 'Hisar'],
    'Himachal Pradesh': ['Shimla', 'Dharamshala', 'Mandi', 'Solan'],
    'Jammu and Kashmir': ['Srinagar', 'Jammu', 'Anantnag', 'Baramulla'],
    'Jharkhand': ['Ranchi', 'Jamshedpur', 'Dhanbad', 'Bokaro'],
    'Karnataka': ['Bengaluru', 'Mysuru', 'Mangaluru', 'Hubballi', 'Belagavi'],
    'Kerala': ['Kochi', 'Kozhikode', 'Thiruvananthapuram', 'Thrissur', 'Kollam'],
    'Ladakh': ['Leh', 'Kargil'],
    'Lakshadweep': ['Kavaratti', 'Agatti', 'Minicoy'],
    'Madhya Pradesh': ['Bhopal', 'Indore', 'Jabalpur', 'Gwalior', 'Ujjain'],
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Kolhapur'],
    'Manipur': ['Imphal', 'Thoubal', 'Bishnupur'],
    'Meghalaya': ['Shillong', 'Tura', 'Jowai'],
    'Mizoram': ['Aizawl', 'Lunglei', 'Champhai'],
    'Nagaland': ['Kohima', 'Dimapur', 'Mokokchung'],
    'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela', 'Puri', 'Sambalpur'],
    'Puducherry': ['Puducherry', 'Karaikal', 'Mahe'],
    'Punjab': ['Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala', 'Bathinda'],
    'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer', 'Bikaner'],
    'Sikkim': ['Gangtok', 'Namchi', 'Gyalshing'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli'],
    'Telangana': ['Hyderabad', 'Warangal', 'Nizamabad', 'Karimnagar'],
    'Tripura': ['Agartala', 'Udaipur', 'Dharmanagar'],
    'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Varanasi', 'Noida', 'Agra', 'Prayagraj'],
    'Uttarakhand': ['Dehradun', 'Haridwar', 'Haldwani', 'Roorkee'],
    'West Bengal': ['Kolkata', 'Siliguri', 'Durgapur', 'Howrah', 'Asansol']
  };

  var PREFIXES = [
    'KrushiSarathi Soil Unit',
    'Agro Soil Diagnostics',
    'Bhoomi Testing Centre',
    'Precision Agri Lab',
    'Krishi Field Lab',
    'Harvest Soil Services',
    'Mitti Analytics Lab'
  ];

  var FIRST = ['Amit', 'Priya', 'Ravi', 'Sneha', 'Kiran', 'Anita', 'Vikash', 'Meera', 'Rajesh', 'Sunita', 'Deepak', 'Neha', 'Arun', 'Divya', 'Manoj', 'Kavita'];
  var LAST = ['K.', 'S.', 'R.', 'P.', 'M.', 'T.', 'N.', 'L.', 'Y.', 'G.'];

  function hashCode(s) {
    var h = 0;
    var i;
    for (i = 0; i < s.length; i++) {
      h = ((h << 5) - h) + s.charCodeAt(i);
      h |= 0;
    }
    return Math.abs(h);
  }

  function buildLabsForCity(state, city) {
    var base = hashCode(state + '|' + city);
    var count = 2 + (base % 2);
    var labs = [];
    var i;
    var seed;
    var pname;
    var contact;
    var day;
    var month;
    var phoneSuffix;
    var visitDate;

    for (i = 0; i < count; i++) {
      seed = base * 7919 + i * 9973;
      pname = PREFIXES[seed % PREFIXES.length];
      contact = FIRST[seed % FIRST.length] + ' ' + LAST[(seed >> 3) % LAST.length];
      day = 8 + (seed % 20);
      month = 5 + (seed % 5);
      phoneSuffix = String(10000 + (seed % 90000));
      visitDate = '2026-' + String(month).padStart(2, '0') + '-' + String(day).padStart(2, '0');

      labs.push({
        name: pname + ' #' + (i + 1) + ' — ' + city,
        city: city,
        state: state,
        contactPerson: contact,
        visitDate: visitDate,
        contactNumber: '+91 98765' + phoneSuffix.slice(-5)
      });
    }
    return labs;
  }

  var allLabs = [];
  var st;
  var cities;
  var ci;
  var city;
  var generated;
  var g;

  for (st in window.CITIES_BY_STATE) {
    if (!Object.prototype.hasOwnProperty.call(window.CITIES_BY_STATE, st)) {
      continue;
    }
    cities = window.CITIES_BY_STATE[st];
    for (ci = 0; ci < cities.length; ci++) {
      city = cities[ci];
      generated = buildLabsForCity(st, city);
      for (g = 0; g < generated.length; g++) {
        allLabs.push(generated[g]);
      }
    }
  }

  window.SOIL_LABS_INDIA = allLabs;
})();
