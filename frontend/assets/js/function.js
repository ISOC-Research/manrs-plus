function formatMetrics(metrics) {
  return `Filtering: ${metrics.filtering}\nCoordination: ${metrics.coordination}\nAntispoofing: ${metrics.antispoofing}\nIRR: ${metrics.irr}\nRPKI: ${metrics.rpki}\nROV: ${metrics.rov}\nSCORE: ${metrics.score}`;
}

function filteringColor(filtering) {
  if (filtering <= 1.5 ) {
    return `<span class="fw-bold">Filtering </span> <i class="bi bi-circle-fill text-success"></i>`
  }else if (filtering > 1.5 && filtering < 5) {
    return `<span class="fw-bold">Filtering </span> <i class="bi bi-circle-fill text-warning"></i>`
  }else if (filtering >= 5) {
    return `<span class="fw-bold">Filtering </span> <i class="bi bi-circle-fill text-danger"></i>`
  }
}

function antispoofingColor(antispoofing) {
  if (antispoofing == 0 ) {
    return `<div><span class="fw-bold">A:</span> <i class="bi bi-circle-fill text-success"></i></div>`
  }else if (antispoofing == 0.5) {
    return `<div><span class="fw-bold">A:</span> <i class="bi bi-circle-fill text-warning"></i></div>`
  }else if (antispoofing == 1) {
    return `<div><span class="fw-bold">A:</span> <i class="bi bi-circle-fill text-danger"></i></div>`
  }
}

function coordinationColor(coordination) {
  if (coordination == 1 ) {
    return `<span class="fw-bold">Coordination </span> <i class="bi bi-circle-fill text-success"></i>`
  }else if (coordination == 0) {
    return `<span class="fw-bold">Coordination </span> <i class="bi bi-circle-fill text-danger"></i>`
  }
}

function irrColor(irr) {
  if (irr < 0.5 ) {
    return `<span class="fw-bold">IRR/RPKI </span> <i class="bi bi-circle-fill text-danger"></i>`
  }else if (irr >= 0.5 && irr < 0.8) {
    return `<span class="fw-bold">IRR/RPKI </span> <i class="bi bi-circle-fill text-warning"></i>`
  }else if (irr >= 0.8) {
    return `<span class="fw-bold">IRR/RPKI </span> <i class="bi bi-circle-fill text-success"></i>`
  }
}

function rpkiColor(rpki) {
  if (rpki < 0.5 ) {
    return `<span class="fw-bold">IRR/RPKI </span> <i class="bi bi-circle-fill text-danger"></i>`
  }else if (rpki >= 0.5 && rpki < 0.8) {
    return `<span class="fw-bold">IRR/RPKI </span> <i class="bi bi-circle-fill text-warning"></i>`
  }else if (rpki >= 0.8) { 
    return `<span class="fw-bold">IRR/RPKI </span> <i class="bi bi-circle-fill text-success"></i>`
  }
}
function rovColor(rov) {
  if (rov == 0 ) {
    return `<span class="fw-bold">ROV </span> <i class="bi bi-x-circle text-danger " ></i>`
  }else if (rov > 0){
    return `<span class="fw-bold">ROV </span> <i class="bi bi-check-circle text-success" ></i>`
  }
}
function shortenText(text, charLimit) {
  if (text == null) {
    return ' ';
  }

  if (text.length > charLimit) {
    text = text.slice(0, charLimit) + '...';
  }

  return text;
}


function convertData2(data1) {
  const data2 = {
    tree: {}
  };
  console.log(data1);
  for (const networkId in data1.networks) {
    
    const network = data1.networks[networkId];
    let type = 'type4';
    var irr_rpki = (network.detail.metrics.irr > network.detail.metrics.rpki) ? network.detail.metrics.irr : network.detail.metrics.rpki;
    if (network.detail.metrics.coordination >= 0.8 && network.detail.metrics.coordination >= 0.8 && irr_rpki >= 0.8) {
      compliance = 1;
    } else {
      compliance = 0;
    } 
    const networkNode = {
      nodeName: `AS${networkId} `,
      name: network.detail.name,
      type: type,
      country: network.detail.country,
      category: network.category,
      filtering: network.detail.metrics.filtering,
      coordination: network.detail.metrics.coordination,
      antispoofing: network.detail.metrics.antispoofing,
      irr: network.detail.metrics.irr,
      rpki: network.detail.metrics.rpki,
      rov: network.detail.metrics.rov,
      colorFiltering: filteringColor(network.detail.metrics.filtering),
      colorCoordination: coordinationColor(network.detail.metrics.coordination),
      colorAntispoofing: antispoofingColor(network.detail.metrics.antispoofing),
      colorIrr: irrColor(network.detail.metrics.irr),
      colorRpki: rpkiColor(network.detail.metrics.rpki),
      rov: network.detail.metrics.rov,
      rovColor: rovColor(network.detail.metrics.rov),
      compliance: compliance,
      label: formatMetrics(network.detail.metrics),
      link: {
        name: `Link ${networkId}`,
        nodeName: networkId,
        direction: "ASYN",
      },
      children: []
    };

    for (const providerId in network.providers) {
      const provider = network.providers[providerId];
      let type = 'type4';
  
      var irr_rpki = (provider.detail.metrics.irr >  provider.detail.metrics.rpki) ?  provider.detail.metrics.irr :  provider.detail.metrics.rpki;
      if ( provider.detail.metrics.coordination >= 0.8 &&  provider.detail.metrics.coordination >= 0.8 && irr_rpki >= 0.8) {
        compliance = 1;
      } else {
        compliance = 0;
      }       
      const providerNode = {
        nodeName: `AS${providerId} `,
        name: provider.detail.name,
        type: type,
        country: provider.detail.country,
        category: provider.detail.category,
        filtering: provider.detail.metrics.filtering,
        coordination: provider.detail.metrics.coordination,
        antispoofing: provider.detail.metrics.antispoofing,
        irr: provider.detail.metrics.irr,
        rpki: provider.detail.metrics.rpki,
        rov: provider.detail.metrics.rov,
        colorFiltering: filteringColor(provider.detail.metrics.filtering),
        colorCoordination: coordinationColor(provider.detail.metrics.coordination),
        colorAntispoofing: antispoofingColor(provider.detail.metrics.antispoofing),
        colorIrr: irrColor(provider.detail.metrics.irr),
        colorRpki: rpkiColor(provider.detail.metrics.rpki),
        rovColor: rovColor(provider.detail.metrics.rov),
        compliance: compliance,
        label: formatMetrics(provider.detail.metrics),
        link: {
          name: `Link ${networkId} to ${providerId}`,
          nodeName: providerId,
          direction: "SYNC",
        },
        children: []
      };

      for (const providerL2Id in provider.providers_l2) {
        const providerL2 = provider.providers_l2[providerL2Id];
        let type='type4';
    
        var irr_rpki = (providerL2.detail.metrics.irr >  providerL2.detail.metrics.rpki) ?  providerL2.detail.metrics.irr :  providerL2.detail.metrics.rpki;
        if (providerL2.detail.metrics.coordination >= 0.8 &&  providerL2.detail.metrics.coordination >= 0.8 && irr_rpki >= 0.8) {
          compliance = 1;
        } else {
          compliance = 0;
        }  
        const providerNodeL2 = {
          nodeName: `AS${providerL2Id} `,
          name: providerL2.detail.name,
          type: type,
          country: providerL2.detail.country,
          category: providerL2.detail.category,
          filtering: providerL2.detail.metrics.filtering,
          coordination: providerL2.detail.metrics.coordination,
          antispoofing: providerL2.detail.metrics.antispoofing,
          irr: providerL2.detail.metrics.irr,
          rpki: providerL2.detail.metrics.rpki,
          rov: providerL2.detail.metrics.rov,
          colorFiltering: filteringColor(providerL2.detail.metrics.filtering),
          colorCoordination: coordinationColor(providerL2.detail.metrics.coordination),
          colorAntispoofing: antispoofingColor(providerL2.detail.metrics.antispoofing),
          colorIrr: irrColor(providerL2.detail.metrics.irr),
          colorRpki: rpkiColor(providerL2.detail.metrics.rpki),
          rovColor: rovColor(providerL2.detail.metrics.rov),
          compliance: compliance,
          label: formatMetrics(providerL2.detail.metrics),
          link: {
            name: `Link ${providerId} to ${providerL2Id}`,
            nodeName: providerL2Id,
            direction: "SYNC",
          },
          children: []
        };
        providerNode.children.push(providerNodeL2);
      }

      networkNode.children.push(providerNode);
    }
    data2.tree[networkId] = networkNode;
  }

  return data2;
}
  

function convertModelToSankeyData2(model) {
  const nodesMap = new Map();
  const nodes = [];
  const links = [];

  // Générer les nœuds pour les réseaux et les fournisseurs
  for (const networkId in model.networks) {
    const network = model.networks[networkId];
    const networkASN = network.detail.name || networkId; // Utilisez ASN comme identifiant de nœud si le nom est null

    if (!nodesMap.has(networkASN)) {
      nodesMap.set(networkASN, nodes.length);
      nodes.push({ name: networkASN +" ("+ network.detail.country+")", label: formatMetrics(network.detail.metrics), score: network.detail.metrics.score });
    }

    for (const providerId in network.providers) {
      const provider = network.providers[providerId];
      const providerASN = provider.detail.name || providerId; // Utilisez ASN comme identifiant de nœud si le nom est null

      if (!nodesMap.has(providerASN)) {
        nodesMap.set(providerASN, nodes.length);
        nodes.push({ name: providerASN +" ("+ provider.detail.country+")", label: formatMetrics(provider.detail.metrics), score: network.detail.metrics.score });
      }

      // Calculer la valeur en fonction du nombre de nœuds dans le réseau
      const networkNodeIndex = nodesMap.get(networkASN);
      const networkNode = nodes[networkNodeIndex];
      const networkSize = nodes.filter(node => node.name === networkASN).length;

      links.push({
        source: nodesMap.get(networkASN),
        target: nodesMap.get(providerASN),
        value: 2
      });

      // Vérifier s'il existe des fournisseurs de niveau 2
      if (provider.providers_l2 && Object.keys(provider.providers_l2).length > 0) {
        for (const providerL2Id in provider.providers_l2) {
          const providerL2 = provider.providers_l2[providerL2Id];
          const providerL2ASN = providerL2.detail.name || providerL2Id; // Utilisez ASN comme identifiant de nœud si le nom est null

          if (!nodesMap.has(providerL2ASN)) {
            nodesMap.set(providerL2ASN, nodes.length);
            nodes.push({ name: providerL2ASN +" ("+ providerL2.detail.country+")", label: formatMetrics(providerL2.detail.metrics), score: network.detail.metrics.score });
          }

          // Calculer la valeur en fonction du nombre de nœuds dans le réseau de niveau 2
          const providerNodeIndex = nodesMap.get(providerASN);
          const providerNode = nodes[providerNodeIndex];
          const providerSize = nodes.filter(node => node.name === providerASN).length;

          links.push({
            source: nodesMap.get(providerASN),
            target: nodesMap.get(providerL2ASN),
            value: 2
          });
        }
      }
    }
  }

  return { nodes, links };
}




var nameToCode = {
    "Afghanistan": "AF",
    "Åland Islands": "AX",
    "Albania": "AL",
    "Algeria": "DZ",
    "American Samoa": "AS",
    "Andorra": "AD",
    "Angola": "AO",
    "Anguilla": "AI",
    "Antarctica": "AQ",
    "Antigua and Barbuda": "AG",
    "Argentina": "AR",
    "Armenia": "AM",
    "Aruba": "AW",
    "Australia": "AU",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Bahamas": "BS",
    "Bahrain": "BH",
    "Bangladesh": "BD",
    "Barbados": "BB",
    "Belarus": "BY",
    "Belgium": "BE",
    "Belize": "BZ",
    "Benin": "BJ",
    "Bermuda": "BM",
    "Bhutan": "BT",
    "Bolivia (Plurinational State of)": "BO",
    "Bonaire, Sint Eustatius and Saba": "BQ",
    "Bosnia and Herzegovina": "BA",
    "Botswana": "BW",
    "Bouvet Island": "BV",
    "Brazil": "BR",
    "British Indian Ocean Territory": "IO",
    "Brunei Darussalam": "BN",
    "Bulgaria": "BG",
    "Burkina Faso": "BF",
    "Burundi": "BI",
    "Cabo Verde": "CV",
    "Cambodia": "KH",
    "Cameroon": "CM",
    "Canada": "CA",
    "Cayman Islands": "KY",
    "Central African Republic": "CF",
    "Chad": "TD",
    "Chile": "CL",
    "China": "CN",
    "Christmas Island": "CX",
    "Cocos (Keeling) Islands": "CC",
    "Colombia": "CO",
    "Comoros": "KM",
    "Congo (Democratic Republic of the)": "CD",
    "Congo": "CG",
    "Cook Islands": "CK",
    "Costa Rica": "CR",
    "Côte d'Ivoire": "CI",
    "Croatia": "HR",
    "Cuba": "CU",
    "Curaçao": "CW",
    "Cyprus": "CY",
    "Czech Republic": "CZ",
    "Denmark": "DK",
    "Djibouti": "DJ",
    "Dominica": "DM",
    "Dominican Republic": "DO",
    "Ecuador": "EC",
    "Egypt": "EG",
    "El Salvador": "SV",
    "Equatorial Guinea": "GQ",
    "Eritrea": "ER",
    "Estonia": "EE",
    "Ethiopia": "ET",
    "Falkland Islands (Malvinas)": "FK",
    "Faroe Islands": "FO",
    "Fiji": "FJ",
    "Finland": "FI",
    "France": "FR",
    "French Guiana": "GF",
    "French Polynesia": "PF",
    "French Southern Territories": "TF",
    "Gabon": "GA",
    "Gambia": "GM",
    "Georgia": "GE",
    "Germany": "DE",
    "Ghana": "GH",
    "Gibraltar": "GI",
    "Greece": "GR",
    "Greenland": "GL",
    "Grenada": "GD",
    "Guadeloupe": "GP",
    "Guam": "GU",
    "Guatemala": "GT",
    "Guernsey": "GG",
    "Guinea": "GN",
    "Guinea-Bissau": "GW",
    "Guyana": "GY",
    "Haiti": "HT",
    "Heard Island and McDonald Islands": "HM",
    "Holy See": "VA",
    "Honduras": "HN",
    "Hong Kong": "HK",
    "Hungary": "HU",
    "Iceland": "IS",
    "India": "IN",
    "Indonesia": "ID",
    "Iran (Islamic Republic of)": "IR",
    "Iraq": "IQ",
    "Ireland": "IE",
    "Isle of Man": "IM",
    "Israel": "IL",
    "Italy": "IT",
    "Jamaica": "JM",
    "Japan": "JP",
    "Jersey": "JE",
    "Jordan": "JO",
    "Kazakhstan": "KZ",
    "Kenya": "KE",
    "Kiribati": "KI",
    "Korea (Democratic People's Republic of)": "KP",
    "Korea (Republic of)": "KR",
    "Kuwait": "KW",
    "Kyrgyzstan": "KG",
    "Lao People's Democratic Republic": "LA",
    "Latvia": "LV",
    "Lebanon": "LB",
    "Lesotho": "LS",
    "Liberia": "LR",
    "Libya": "LY",
    "Liechtenstein": "LI",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Macao": "MO",
    "Macedonia (the former Yugoslav Republic of)": "MK",
    "Madagascar": "MG",
    "Malawi": "MW",
    "Malaysia": "MY",
    "Maldives": "MV",
    "Mali": "ML",
    "Malta": "MT",
    "Marshall Islands": "MH",
    "Martinique": "MQ",
    "Mauritania": "MR",
    "Mauritius": "MU",
    "Mayotte": "YT",
    "Mexico": "MX",
    "Micronesia (Federated States of)": "FM",
    "Moldova (Republic of)": "MD",
    "Monaco": "MC",
    "Mongolia": "MN",
    "Montenegro": "ME",
    "Montserrat": "MS",
    "Morocco": "MA",
    "Mozambique": "MZ",
    "Myanmar": "MM",
    "Namibia": "NA",
    "Nauru": "NR",
    "Nepal": "NP",
    "Netherlands": "NL",
    "New Caledonia": "NC",
    "New Zealand": "NZ",
    "Nicaragua": "NI",
    "Niger": "NE",
    "Nigeria": "NG",
    "Niue": "NU",
    "Norfolk Island": "NF",
    "Northern Mariana Islands": "MP",
    "Norway": "NO",
    "Oman": "OM",
    "Pakistan": "PK",
    "Palau": "PW",
    "Palestine, State of": "PS",
    "Panama": "PA",
    "Papua New Guinea": "PG",
    "Paraguay": "PY",
    "Peru": "PE",
    "Philippines": "PH",
    "Pitcairn": "PN",
    "Poland": "PL",
    "Portugal": "PT",
    "Puerto Rico": "PR",
    "Qatar": "QA",
    "Réunion": "RE",
    "Romania": "RO",
    "Russian Federation": "RU",
    "Rwanda": "RW",
    "Saint Barthélemy": "BL",
    "Saint Helena, Ascension and Tristan da Cunha": "SH",
    "Saint Kitts and Nevis": "KN",
    "Saint Lucia": "LC",
    "Saint Martin (French part)": "MF",
    "Saint Pierre and Miquelon": "PM",
    "Saint Vincent and the Grenadines": "VC",
    "Samoa": "WS",
    "San Marino": "SM",
    "Sao Tome and Principe": "ST",
    "Saudi Arabia": "SA",
    "Senegal": "SN",
    "Serbia": "RS",
    "Seychelles": "SC",
    "Sierra Leone": "SL",
    "Singapore": "SG",
    "Sint Maarten (Dutch part)": "SX",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Solomon Islands": "SB",
    "Somalia": "SO",
    "South Africa": "ZA",
    "South Georgia and the South Sandwich Islands": "GS",
    "South Sudan": "SS",
    "Spain": "ES",
    "Sri Lanka": "LK",
    "Sudan": "SD",
    "Suriname": "SR",
    "Svalbard and Jan Mayen": "SJ",
    "Swaziland": "SZ",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Syrian Arab Republic": "SY",
    "Taiwan, Province of China": "TW",
    "Tajikistan": "TJ",
    "Tanzania, United Republic of": "TZ",
    "Thailand": "TH",
    "Timor-Leste": "TL",
    "Togo": "TG",
    "Tokelau": "TK",
    "Tonga": "TO",
    "Trinidad and Tobago": "TT",
    "Tunisia": "TN",
    "Turkey": "TR",
    "Turkmenistan": "TM",
    "Turks and Caicos Islands": "TC",
    "Tuvalu": "TV",
    "Uganda": "UG",
    "Ukraine": "UA",
    "United Arab Emirates": "AE",
    "United Kingdom of Great Britain and Northern Ireland": "GB",
    "United States of America": "US",
    "United States Minor Outlying Islands": "UM",
    "Uruguay": "UY",
    "Uzbekistan": "UZ",
    "Vanuatu": "VU",
    "Venezuela (Bolivarian Republic of)": "VE",
    "Viet Nam": "VN",
    "Virgin Islands (British)": "VG",
    "Virgin Islands (U.S.)": "VI",
    "Wallis and Futuna": "WF",
    "Western Sahara": "EH",
    "Yemen": "YE",
    "Zambia": "ZM",
    "Zimbabwe": "ZW"
  };

  
  function convertCountry(input) {
    if (nameToCode[input]) {
      // Si le paramètre est un nom de pays, renvoyer le code
      return nameToCode[input];
    } else {
      // Si le paramètre est un code de pays, renvoyer le nom
      for (const name in nameToCode) {
        if (nameToCode[name] === input) {
          return name;
        }
      }
    }
    // Si aucune correspondance n'a été trouvée, renvoyer undefined
    return undefined;
  }