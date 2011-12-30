# -*- coding: utf-8 -*-


templates = {
    '': {},
    'test_noargs': {
           'subject': "Test email subject",
           'from_email': "Test Address<admin@beatwrit.com>",
           'body_plain': "Test email body",
           'body_html': """<div>Test html body</div><div>Another <b>line</b></div>""",
    },
    
    'test': {
           'subject': "Test email subject to {{ name }}",
           'from_email': "Test Address<admin@beatwrit.com>",
           'body_plain': "Test email body.  The time is {{ time }}",
           'body_html': "<div>Test html body</div><div>Another <b>line</b> with the color {{ color }}</div>",
    },
            
    'email_confirmation' : {
           'subject': "Confirm your address",
           'from_email': "Beatwrit Accounts<no-reply-confirm@beatwrit.com>",
           'body_plain': "",
           'body_html': """

<html lang="en">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
    <title>
        TITLE HERE 
    </title>
    <style type="text/css">
    </style>
  </head>
<body>
    <p>Hi {{ penname }},<p>
    <br/>
    <p>Many thanks for joining Beatwrit, the lightweight collaborative writing game.  Your account setup is nearly complete.  The only step left is to confirm your email address.  This isn't required, but is useful because 1) we send you email reminders when it becomes your turn in a writ and 2) your email can be used to recover your account password in the event that you lose it.</p>

    To confirm your email, click the following link:<br/>
    <a href='{{ email_confirm_url }}'>Confirm address</a><br/>
    <br/>
    If the link above does not display, you can simply copy and paste this url into your browser:<br/>
    {{ email_confirm_url }}<br/>
    <br/>
    <br/>

    ^beatwrit<br/>
    --------------------------------------------<br/> 
    <br/> 
    <br/> 
    If you wish to reduce the number of emails you receive from us, simply access your account settings page and change the options under the email tab.<br/>
</body>
"""
    },
    
    'turn_reminder' : {
           'subject': "{% load mainfilters %}Your turn in a writ | {{ first_line|truncate_words_by_maxchars:30 }}...",
           'from_email': "Beatwrit Reminders<no-reply-reminders@beatwrit.com",
           'body_plain': "",
           'body_html': """
<html lang="en">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
    <title>
        TITLE HERE 
    </title>
    <style type="text/css">
    p {font-size: 15pt;}
    p.footer {font-size: 9pt;}
    </style>
  </head>
<body>
    
    <p style='color: #111'>Hi {{ penname }},</p>

    <p style='color: #111'>It's your turn to contribute in the writ that begins with the line "{{ first_line }}..."  Click this link to <a href='{{ direct_login_link }}'>automatically login</a> and contribute.</p>

    <p style='color: #111'>^beatwrit</p>
    <br/> 
    --------------------------------------------<br/> 
    <p style='font-size: 9pt; color: #333333;'>We promise we want to avoid sending too many emails, but if you wish to reduce the number of emails you receive from us, simply access your account settings page and change the options under the email tab.</p>
</body>
""",
    },

    'inactive_reminder' : {
           'subject': "{% load mainfilters %}A writ is getting cold | {{ first_line|truncate_words_by_maxchars:30 }}...",
           'from_email': "Beatwrit Reminders<no-reply-reminders@beatwrit.com",
           'body_plain': "",
           'body_html': """
<html lang="en">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
    <title>
        TITLE HERE 
    </title>
    <style type="text/css">
    * {font-size: 10pt;}
    .footer {font-size: 9pt;}
    </style>
  </head>
<body>
    <p>Hi {{ penname }},</p>

    <p>Your writ that begins with "{{ first_line }}..." hasn't been contributed to in some time.  If you don't want it to close due to inactivity, you might want to <a href='{{ direct_login_link }}'>automatically login</a> and contribute something to get it going again.  

    ~beatwrit.com
    
    --------------------------------------------<br/> 
    <br/> 
    <br/> 
    <p class='footer'>If you wish to reduce the number of emails you receive from us, simply access your account settings page and change the options under the email tab.</p>
</body>
""",
    },


}



test_body_html = """
<html lang="en">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
    <title>
      Boutique
    </title>
    <style type="text/css">
    </style>
  </head>
  <body style="margin: 0; padding: 0; background: #f3dc74 url('images/bg_email.jpg') no-repeat center top;" bgcolor="#f3dc74">
    <table cellpadding="0" cellspacing="0" border="0" align="center" width="100%" style="background: url('images/bg_email.jpg') no-repeat center top; padding: 85px 0 35px">
          <tr>
            <td align="center">
                <table cellpadding="0" cellspacing="0" border="0" align="center" width="599" style="font-family: Georgia, serif; background: url('images/bg_header.jpg') no-repeat center top" height="142">
                  <tr>
                    <td style="margin: 0; padding: 40px 0 0; background: #c89c22 url('images/bg_header.jpg') no-repeat center top" align="center" valign="top">
                        <h1 style="color: #ede6cb; font: normal 24px Georgia, serif; margin: 0; padding: 0; line-height: 28px;">Grandma's Sweets &amp; Cookies</h1>
                    </td>
                  </tr>
                  <tr>
                    <td style="margin: 0; padding: 25px 0 0;" align="center" valign="top">
                        <p style="color: #645847; font: bold 11px Georgia, serif; margin: 0; padding: 0; line-height: 12px; text-transform: uppercase;">ESTABLISHED 1405</p>
                    </td>
                  </tr>
                  <tr>
                      <td style="font-size: 1px; height: 15px; line-height: 1px;" height="15">&nbsp;</td>
                  </tr> 
                </table><!-- header-->
                <table cellpadding="0" cellspacing="0" border="0" align="center" width="599" style="font-family: Georgia, serif;" >
                  <tr>
                    <td width="599" valign="top" align="left" bgcolor="#ffffff"style="font-family: Georgia, serif; background: #fff; border-top: 5px solid #e5bd5f">
                        <table cellpadding="0" cellspacing="0" border="0"  style="color: #717171; font: normal 11px Georgia, serif; margin: 0; padding: 0;" width="599">
                        <tr>
                            <td width="15" style="font-size: 1px; line-height: 1px; width: 15px;"><img src="images/spacer.gif" alt="space" width="15"></td>
                            <td style="padding: 15px 0 5px; font-family: Georgia, serif;" valign="top" align="center" width="569">
                                <img src="images/divider_top_full.png" alt="divider"><br>
                                <h3 style="color:#c58123; font-weight: bold; text-transform: uppercase; margin: 0; padding: 0; line-height: 22px; font-size: 10px;"><$currentdayname$> <$currentday$> <$currentmonthname$></h3>
                            </td>
                            <td width="15" style="font-size: 1px; line-height: 1px; width: 15px;"><img src="images/spacer.gif" alt="space" width="15"></td>
                        </tr>
                        <tr>
                            <td width="15" style="font-size: 1px; line-height: 1px; width: 15px;"><img src="images/spacer.gif" alt="space" width="15"></td>
                            <td style="padding: 10px 0 0; font-family: Helvetica, Arial, sans-serif;" align="left">         
                                <h2 style="color:#393023; font-weight: bold; margin: 0; padding: 0; line-height: 30px; font-size: 17px;font-family: Helvetica, Arial, sans-serif;">Meet Jack — a brown cow.</h2>
                                <p style="color:#767676; font-weight: normal; margin: 0; padding: 0; line-height: 20px; font-size: 12px;">
                                    Suspendisse potenti--Fusce eu ante in sapien vestibulum sagittis. Cras purus. Nunc rhoncus. <a href="#" style="color: #0fa2e6; text-decoration: none;">Donec imperdiet</a>, nibh sit amet pharetra placerat, tortor purus condimentum lectus.
                                </p>
                            </td>
                            <td width="15" style="font-size: 1px; line-height: 1px; width: 15px;"><img src="images/spacer.gif" alt="space" width="15"></td>
                        </tr>
                        <tr>
                            <td width="15" style="font-size: 1px; line-height: 1px; width: 15px;"><img src="images/spacer.gif" alt="space" width="15"></td>
                            <td style="padding: 10px 0 0; font-family: Helvetica, Arial, sans-serif;" align="left">     
                                <img src="images/img.jpg" alt="Cow" style="border: 5px solid #f7f7f4;">
                            </td>
                        </tr>
                        <tr>
                            <td width="15" style="font-size: 1px; line-height: 1px; width: 15px;"><img src="images/spacer.gif" alt="space" width="15"></td>
                            <td style="padding: 10px 0 0; font-family: Helvetica, Arial, sans-serif;" align="left">         
                                <p style="color:#767676; font-weight: normal; margin: 0; padding: 0; line-height: 20px; font-size: 12px;">
                                    Suspendisse potenti--Fusce eu <a href="#" style="color: #0fa2e6; text-decoration: none;">ante in sapien</a> vestibulum sagittis.
                                </p>
                            </td>
                        </tr>
                        <tr>
                            <td width="15" style="font-size: 1px; line-height: 1px; width: 15px;"><img src="images/spacer.gif" alt="space" width="15"></td>
                            <td style="padding: 10px 0 0; font-family: Helvetica, Arial, sans-serif;" align="left">
                                <img src="images/divider_full.png" alt="divider">
                            </td>
                            <td width="15" style="font-size: 1px; line-height: 1px; width: 15px;"><img src="images/spacer.gif" alt="space" width="15"></td>
                        </tr>
                        <tr>
                            <td width="15" style="font-size: 1px; line-height: 1px; width: 15px;"><img src="images/spacer.gif" alt="space" width="15"></td>
                            <td style="padding: 10px 0 55px; font-family: Helvetica, Arial, sans-serif;" align="left">          
                                <h2 style="color:#393023; font-weight: bold; margin: 0; padding: 0; line-height: 30px; font-size: 17px;font-family: Helvetica, Arial, sans-serif;">Cookies feels more valuable now 
                                than before</h2>
                                <p style="color:#767676; font-weight: normal; margin: 0; padding: 0; line-height: 20px; font-size: 12px;">
                                    Suspendisse potenti--Fusce eu ante in sapien vestibulum sagittis. Cras purus. Nunc rhoncus. Donec imperdiet, nibh sit amet pharetra placerat, tortor purus condimentum lectus. Says Doctor Lichtenstein in an interview done after last nights press conference in Belgium.
                                    <a href="#" style="color: #0fa2e6; text-decoration: none;">Dr. Lichtenstein</a> also states his concerns regarding chocolate now suddenly turning yellow the last couple of years. 
                                </p>
                            </td>
                        </tr>  
                        </table>    
                    </td>
                  </tr>
                 <tr>
                      <td style="font-size: 1px; height: 10px; line-height: 1px;" height="10"><img src="images/spacer.gif" alt="space" width="15"></td>
                  </tr>
                </table><!-- body -->
                <table cellpadding="0" cellspacing="0" border="0" align="center" width="599" style="font-family: Georgia, serif; line-height: 10px;" bgcolor="#464646" class="footer">
                  <tr>
                    <td bgcolor="#464646"  align="center" style="padding: 15px 0 10px; font-size: 11px; color:#bfbfbf; margin: 0; line-height: 1.2;font-family: Helvetica, Arial, sans-serif;" valign="top">
                        <p style="font-size: 11px; color:#bfbfbf; margin: 0; padding: 0;font-family: Helvetica, Arial, sans-serif;">You're receiving this newsletter because you bought widgets from us. </p>
                        <p style="font-size: 11px; color:#bfbfbf; margin: 0 0 10px 0; padding: 0;font-family: Helvetica, Arial, sans-serif;">Having trouble reading this? <webversion style="color: #0fa2e6; text-decoration: none;">View it in your browser</webversion>. Not interested anymore? <unsubscribe style="color: #0fa2e6; text-decoration: none;">Unsubscribe</unsubscribe> Instantly.</p>
                    </td>
                  </tr>
                  <tr> 
                </table><!-- footer-->
            </td>
        </tr>
    </table>
  </body>
</html>

"""





















test_body_html2 = """
<html>
<body leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0" bgcolor='#99CC00' >

<STYLE>
 .headerTop { background-color:#FFCC66; border-top:0px solid #000000; border-bottom:1px solid #FFFFFF; text-align:center; }
 .adminText { font-size:10px; color:#996600; line-height:200%; font-family:verdana; text-decoration:none; }
 .headerBar { background-color:#FFFFFF; border-top:0px solid #333333; border-bottom:10px solid #FFFFFF; }
 .title { font-size:20px; font-weight:bold; color:#CC6600; font-family:arial; line-height:110%; }
 .subTitle { font-size:11px; font-weight:normal; color:#666666; font-style:italic; font-family:arial; }
 td { font-size:12px; color:#000000; line-height:150%; font-family:trebuchet ms; }
 .sideColumn { background-color:#FFFFFF; border-left:1px dashed #CCCCCC; text-align:left; }
 .sideColumnText { font-size:11px; font-weight:normal; color:#999999; font-family:arial; line-height:150%; }
 .sideColumnTitle { font-size:15px; font-weight:bold; color:#333333; font-family:arial; line-height:150%; }
 .footerRow { background-color:#FFFFCC; border-top:10px solid #FFFFFF; }
 .footerText { font-size:10px; color:#996600; line-height:100%; font-family:verdana; }
 a { color:#FF6600; color:#FF6600; color:#FF6600; }
</STYLE>



<table width="100%" cellpadding="10" cellspacing="0" bgcolor='#99CC00' >
<tr>
<td valign="top" align="center">

<table width="600" cellpadding="0" cellspacing="0">
<tr>
<td style="background-color:#FFCC66;border-top:0px solid #000000;border-bottom:1px solid #FFFFFF;text-align:center;" align="center"><span style="font-size:10px;color:#996600;line-height:200%;font-family:verdana;text-decoration:none;">Email not displaying correctly? <a href="*|ARCHIVE|*" style="font-size:10px;color:#996600;line-height:200%;font-family:verdana;text-decoration:none;">View it in your browser.</a></span></td>

</tr>

<tr>
<td align="left" valign="middle" style="background-color:#FFFFFF;border-top:0px solid #333333;border-bottom:10px solid #FFFFFF;"><center><a href=""><IMG id=editableImg1 SRC="img/logo_2column.jpg" BORDER="0" title="Your Company"  alt="Your Company" align="center"></a></center></td>
</tr>


</table>

<table width="600" cellpadding="20" cellspacing="0" bgcolor="#FFFFFF">
<tr>

<td bgcolor="#FFFFFF" valign="top" width="400" style="font-size:12px;color:#000000;line-height:150%;font-family:trebuchet ms;">

<p>
<span style="font-size:20px;font-weight:bold;color:#CC6600;font-family:arial;line-height:110%;">Why Are Tigers So Mean?</span><br>

<span style="font-size:11px;font-weight:normal;color:#666666;font-style:italic;font-family:arial;">by Frederick Von Chimpenheimer</span><br>
Recent psychological studies and brain scans have shown that tigers have naturally violent tendencies toward chimpanzees. "There's sort of a banana-envy thing going on, which makes the average tiger very self-conscious around chimpanzees" says Dr. Chimpfried Brown. Lorem ipsum dolor sit amet, <a href="#">consectetuer adipiscing elit</a>. Sed at erat. Phasellus condimentum. Nullam sed magna. Donec quis tellus in neque congue porttitor. Proin sit amet ligula id leo porta rutrum. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. In suscipit, pede a rutrum malesuada, lacus massa euismod neque, a hendrerit justo ante at eros. <a href="#">Clickitus heritus.</a>
</p>



<p>
<span style="font-size:20px;font-weight:bold;color:#CC6600;font-family:arial;line-height:110%;">Plantains vs. Bananas</span><br>
<span style="font-size:11px;font-weight:normal;color:#666666;font-style:italic;font-family:arial;">by Francine Chimperson</span><br>
Throwing a party? There's no better way to anger your dinner guests than by accidentally serving them plantains instead of bananas. Avoid the poo flinging with these handy guidelines. Plantains look like over ripe bananas, and must be cooked before eaten. Bananas are softer, and don't cook very well (they get mushy). In suscipit, pede a rutrum malesuada, lacus massa euismod neque <a href="#">Clickitus heritus.</a>

</p>

</td>


<td width="200" valign="top" style="background-color:#FFFFFF;border-left:1px dashed #CCCCCC;text-align:left;">
<span style="font-size:11px;font-weight:normal;color:#999999;font-family:arial;line-height:150%;">

<span style="font-size:15px;font-weight:bold;color:#333333;font-family:arial;line-height:150%;">Grooming Tips:</span><br>
Tick picking novice? Lorem ipsum dolor sit amet, <a href="#">consectetuer adipiscing elit</a>. Sed at erat. Phasellus condimentum. Nullam sed magna. Donec quis tellus in neque congue porttitor. Proin sit amet ligula id leo porta rutrum.

<br>
<br>

<span style="font-size:15px;font-weight:bold;color:#333333;font-family:arial;line-height:150%;">Waterhole Dangers</span><br>

Watery oasis, or crocodilian cesspool from hell? As the dry season approaches, lorem ipsum dolor sit amet, <a href="#">consectetuer adipiscing elit</a>. Sed at erat. Phasellus condimentum. Nullam sed magna. Donec quis tellus in neque congue porttitor. Proin sit amet ligula id leo porta rutrum.

</span>
</td>


</tr>


<tr>
<td style="background-color:#FFFFCC;border-top:10px solid #FFFFFF;" valign="top" colspan="2">
<span style="font-size:10px;color:#996600;line-height:100%;font-family:verdana;">
*|LIST:DESCRIPTION|* <br />
<br />
<a href="*|UNSUB|*">Unsubscribe</a> *|EMAIL|* from this list.<br />

<br />
Our mailing address is:<br />
*|LIST:ADDRESS|*<br />
<br />
Our telephone:<br />
*|LIST:PHONE|*<br />
<br />
Copyright (C) 2007 *|LIST:COMPANY|* All rights reserved.<br />
<br />
<a href="*|FORWARD|*">Forward</a> this email to a friend
  

</span>
</td>
</tr>


</table>







</td>
</tr>
</table>




</body>
</html>
"""
