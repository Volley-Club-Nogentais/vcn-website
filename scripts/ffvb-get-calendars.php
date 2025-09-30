$Current = Date('N');
$Sunday = Date('d/m/y', StrToTime("- {$Current} Days"));
$Current++;
$Saturday = Date('d/m/y', StrToTime("- {$Current} Days"));

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "http://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php?saison=2016/2017&codent=PTIDF94&poule=SMI");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$ffvb = curl_exec ($ch);

preg_match_all("/<table.*?>(.*?)<\/table>/si", $ffvb, $ffvbTable);

$tabJournee = $ffvbTable[0][2];

preg_match_all("/<tr.*?>(.*?)<\/tr>/si", $tabJournee, $ffvbTR);

echo "<table>";

//Dep 1
for ($i = 0; $i < count($ffvbTR[0]); $i++) {
   preg_match_all("/(".str_replace("/", "\/", $Sunday)."|".str_replace("/", "\/", $Saturday).")/si", $ffvbTR[0][$i], $output_array);
   if (count($output_array[0]) > 0) {
      $pos = strrpos($ffvbTR[0][$i],"NOGENT- LE PERREUX 1");
      if ($pos === false) {
          // non trouvé ...
      }
      else {
$td = $ffvbTR[0][$i];
preg_match_all("/<td.*?>(.*?)<\/td>/si", $td, $resultats);

if ($resultats[1][6] < $resultats[1][7]) {
$boldLeft = "";
$boldRight = "<b>";
}
else {
$boldLeft = "<b>";
$boldRight = "";
}

$pos = strrpos($resultats[1][3],"NOGENT- LE PERREUX 1");
if ($pos === false) {
echo "<tr><td width=50%><font size=1>" . $boldLeft . $resultats[1][3] . "</b></font></td><td width=50%><font size=1>" . $boldRight . " Dép.1 Homme</b></font></td></tr>";
}
else {
echo "<tr><td width=50%><font size=1>" . $boldLeft . "Dép.1 Homme" . "</b></font></td><td width=50%><font size=1>" . $boldRight . $resultats[1][5]. "</font></td></tr>";
}
echo "<tr><td align=center><font size=1>" . $resultats[1][6] . "</font></td><td><font size=1>" . $resultats[1][7] . "</font></td></tr>";
echo '<tr><td colspan=2><font size=1>' . $resultats[1][8].'</font></td></tr>';
echo '<tr><td colspan=2><hr></td></tr>';
      }
   }
}

//Dep 2
for ($i = 0; $i < count($ffvbTR[0]); $i++) {
   preg_match_all("/(".str_replace("/", "\/", $Sunday)."|".str_replace("/", "\/", $Saturday).")/si", $ffvbTR[0][$i], $output_array);
   if (count($output_array[0]) > 0) {
      $pos = strrpos($ffvbTR[0][$i],"NOGENT-LE PERREUX 2");
      if ($pos === false) {
          // non trouvé ...
      }
      else {
$td = $ffvbTR[0][$i];
preg_match_all("/<td.*?>(.*?)<\/td>/si", $td, $resultats);

if ($resultats[1][6] < $resultats[1][7]) {
$boldLeft = "";
$boldRight = "<b>";
}
else {
$boldLeft = "<b>";
$boldRight = "";
}

$pos = strrpos($resultats[1][3],"NOGENT-LE PERREUX 2");
if ($pos === false) {
echo "<tr><td width=50%><font size=1>" . $boldLeft . $resultats[1][3] . "</b></font></td><td width=50%><font size=1>" . $boldRight . " Dép.2 Homme</b></font></td></tr>";
}
else {
echo "<tr><td width=50%><font size=1>" . $boldLeft . "Dép.2 Homme" . "</b></font></td><td width=50%><font size=1>" . $boldRight . $resultats[1][5]. "</font></td></tr>";
}
                 if (is_numeric($resultats[1][6])) {
    echo "<tr><td align=center><font size=1>" . $resultats[1][6] . "</font></td><td><font size=1>" . $resultats[1][7] . "</font></td></tr>";
    echo '<tr><td colspan=2><font size=1>' . $resultats[1][8].'</font></td></tr>';
                 }
echo '<tr><td colspan=2><hr></td></tr>';
      }
   }
}

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "http://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php?saison=2016/2017&codent=LIIDF&poule=PFA");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$ffvb = curl_exec ($ch);

preg_match_all("/<table.*?>(.*?)<\/table>/si", $ffvb, $ffvbTable);

$tabJournee = $ffvbTable[0][2];

preg_match_all("/<tr.*?>(.*?)<\/tr>/si", $tabJournee, $ffvbTR);

for ($i = 0; $i < count($ffvbTR[0]); $i++) {
   preg_match_all("/(".str_replace("/", "\/", $Sunday)."|".str_replace("/", "\/", $Saturday).")/si", $ffvbTR[0][$i], $output_array);
   if (count($output_array[0]) > 0) {
      $pos = strrpos($ffvbTR[0][$i],"NOGENT");
      if ($pos === false) {
          // non trouvé ...
      }
      else {
$td = $ffvbTR[0][$i];
preg_match_all("/<td.*?>(.*?)<\/td>/si", $td, $resultats);

if ($resultats[1][6] < $resultats[1][7]) {
$boldLeft = "";
$boldRight = "<b>";
}
else {
$boldLeft = "<b>";
$boldRight = "";
}

$pos = strrpos($resultats[1][3],"NOGENT");
if ($pos === false) {
echo "<tr><td width=50%><font size=1>" . $boldLeft . $resultats[1][3] . "</b></font></td><td width=50%><font size=1>" . $boldRight . " Pré-Nat. Fem.</b></font></td></tr>";
}
else {
echo "<tr><td width=50%><font size=1>" . $boldLeft . "Pré. nat. Fem." . "</b></font></td><td width=50%><font size=1>" . $boldRight . $resultats[1][5]. "</b></font></td></tr>";
}
echo "<tr><td align=center><font size=1>" . $resultats[1][6] . "</font></td><td><font size=1>" . $resultats[1][7] . "</font></td></tr>";
echo "<tr><td colspan=2><font size=1>" . $resultats[1][8]."</font></td></tr>";
echo '<tr><td colspan=2><hr></td></tr>';
      }
   }
}

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "http://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php?saison=2016%2F2017&codent=PTIDF94&poule=SFI");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$ffvb = curl_exec ($ch);

preg_match_all("/<table.*?>(.*?)<\/table>/si", $ffvb, $ffvbTable);

$tabJournee = $ffvbTable[0][2];

preg_match_all("/<tr.*?>(.*?)<\/tr>/si", $tabJournee, $ffvbTR);

for ($i = 0; $i < count($ffvbTR[0]); $i++) {
   preg_match_all("/(".str_replace("/", "\/", $Sunday)."|".str_replace("/", "\/", $Saturday).")/si", $ffvbTR[0][$i], $output_array);
   if (count($output_array[0]) > 0) {
      $pos = strrpos($ffvbTR[0][$i],"NOGENT");
      if ($pos === false) {
          // non trouvé ...
      }
      else {
$td = $ffvbTR[0][$i];
preg_match_all("/<td.*?>(.*?)<\/td>/si", $td, $resultats);

if ($resultats[1][6] < $resultats[1][7]) {
$boldLeft = "";
$boldRight = "<b>";
}
else {
$boldLeft = "<b>";
$boldRight = "";
}

$pos = strrpos($resultats[1][3],"NOGENT");
if ($pos === false) {
echo "<tr><td width=50%><font size=1>" . $boldLeft . $resultats[1][3] . "</b></font></td><td width=50%><font size=1>" . $boldRight . " Dép. Fem.</b></font></td></tr>";
}
else {
echo "<tr><td width=50%><font size=1>" . $boldLeft . "Dép. Fem." . "</b></font></td><td width=50%><font size=1>" . $boldRight . $resultats[1][5]. "</b></font></td></tr>";
}
echo "<tr><td align=center><font size=1>" . $resultats[1][6] . "</font></td><td><font size=1>" . $resultats[1][7] . "</font></td></tr>";
echo "<tr><td colspan=2><font size=1>" . $resultats[1][8]."</font></td></tr>";
echo '<tr><td colspan=2><hr></td></tr>';
      }
   }
}

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "http://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php?saison=2015/2016&codent=PTIDF94&poule=SMI");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$ffvb = curl_exec ($ch);

preg_match_all("/<table.*?>(.*?)<\/table>/si", $ffvb, $ffvbTable);

$tabJournee = $ffvbTable[0][2];

preg_match_all("/<tr.*?>(.*?)<\/tr>/si", $tabJournee, $ffvbTR);

for ($i = 0; $i < count($ffvbTR[0]); $i++) {
   preg_match_all("/(".str_replace("/", "\/", $Sunday)."|".str_replace("/", "\/", $Saturday).")/si", $ffvbTR[0][$i], $output_array);
   if (count($output_array[0]) > 0) {
      $pos = strrpos($ffvbTR[0][$i],"PERREUX");
      if ($pos === false) {
          // non trouvé ...
      }
      else {
$td = $ffvbTR[0][$i];
preg_match_all("/<td.*?>(.*?)<\/td>/si", $td, $resultats);

if ($resultats[1][6] < $resultats[1][7]) {
$boldLeft = "";
$boldRight = "<b>";
}
else {
$boldLeft = "<b>";
$boldRight = "";
}

$pos = strrpos($resultats[1][3],"PERREUX");
if ($pos === false) {
echo "<tr><td width=50%><font size=1>" . $boldLeft . $resultats[1][3] . "</b></font></td><td width=50%><font size=1>" . $boldRight . " Dép. Homme</b></font></td></tr>";
}
else {
echo "<tr><td width=50%><font size=1>" . $boldLeft . "Dép. Homme" . "</b></font></td><td width=50%><font size=1>" . $boldRight . $resultats[1][5]. "</b></font></td></tr>";
}
echo "<tr><td align=center><font size=1>" . $resultats[1][6] . "</font></td><td><font size=1>" . $resultats[1][7] . "</font></td></tr>";
echo "<tr><td colspan=2><font size=1>" . $resultats[1][8]."</font></td></tr>";
echo '<tr><td colspan=2><hr></td></tr>';
      }
   }
}
echo "</table>";
