using System;
using WangZhuan.BaseFormLayout;
using Lj.Common;
using System.Net;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Text.RegularExpressions;
using System.Globalization;
using System.Collections.Generic;
namespace WangZhuan
{
    [CommandMeta("惠人贷签到", 1)]
    public class 惠人贷签到 : BaseMenuCommnad
    {


        protected override bool Run(AutoTaskContext task)
        {

          
            string html = string.Empty;

            var headers = CreateHeaders("http://www.huirendai.com/index.php");
            headers["Upgrade-Insecure-Requests"] = "1";
            var post = "http://www.huirendai.com/index.php?user&q=action/login";

            //TcpClient clientSocket = new TcpClient();
            //Uri URI = new Uri(post);
            //clientSocket.Connect(URI.Host, URI.Port);
            //StringBuilder requestHeaders = new StringBuilder();
            //requestHeaders.Append("GET /index.php?user&q=action/login HTTP/1.1\r\n");
            //requestHeaders.Append("Host:www.huirendai.com\r\n");
            //requestHeaders.Append("Connection:keep-alive\r\n");
            //requestHeaders.Append("Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n");
            //requestHeaders.Append("Upgrade-Insecure-Requests:1\r\n");
            //requestHeaders.Append("User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)\r\n");
            //requestHeaders.Append("Accept-Language:zh-CN,zh;q=0.8\r\n\r\n");

            //byte[] request = Encoding.UTF8.GetBytes(requestHeaders.ToString());
            //clientSocket.Client.Send(request);
            //byte[] responseByte = new byte[1024000];
            //logger.Info("数据接收中...");
            //int len = clientSocket.Client.Receive(responseByte);
            //string rs = Encoding.UTF8.GetString(responseByte, 0, len);
            //logger.Info(rs);
            //var ck = Regex.Match(rs, "__jsluid=(.*);").Get(1);
            //logger.Info(ck);
            //var code = Regex.Match(rs, @"<script>(.*)<\/script>").Get(1);
            //code = " var code = ''; " + code;
            //code = code.Replace("return p;", "code = p;return function(){};");
            //code = code.Replace("document.cookie=dc;", "");
            //var para = "";
            //code = Regex.Replace(code, @"(.*\()(.*)(\))", m =>
            //{
            //    para = m.Get(2);
            //    return m.Get(1) + m.Get(3);
            //});
            //code = "var rn = function(){ " + code + ";return code; }";
            //var rt = ExecuteScript("rn()", code);
            
            //rt = Regex.Replace(rt, "(.*)setTimeout.*", "$1");
            //rt = "var dc='';var t_d={hello:'world',t_c:function(x){if(x===''){return}if(x.slice(-1)===';'){x=x+' '}if(x.slice(-2)!=='; '){x=x+'; '}dc=dc+x}};var a = " + para + "; " + rt;
            //rt = "var j = function(){ " + rt + ";return dc; }";
            //var j = ExecuteScript("j()", rt);

            //clientSocket.Close();
            //logger.Info(j);
            //var jv = Regex.Match(j, "__jsl_clearance=(.*?);").Get(1);
            //var expires = Regex.Match(j, @"Expires=.*,\s+(.*?)\s+GMT;").Get(1);
            //var expiresItems = expires.Split(' ');
            //var items = expiresItems[0].Split('-');
            //var timeText = string.Format("{0}-{1}-{2} {3}", items[2], items[1], items[0], expiresItems[1]);
            //logger.Info(timeText);
            ////var dt = DateTime.Parse(expires).AddHours(7);
            //CultureInfo cultureInfo = CultureInfo.CreateSpecificCulture("en-US");
            ////Mon, 17-Aug-15 06:04:18 GMT

            //DateTime dt = DateTime.Parse(timeText);
            //dt = dt.AddHours(7);
            //// 得到日期字符串 DateTime datetime = DateTime.ParseExact("Wed Aug 25 16:28:03 +0800 2010", format, cultureInfo); // 将字符串转换成日期
            //logger.Info(dt.ToString());
            //var __jsl_clearance = new Cookie("__jsl_clearance", jv, "/", "www.huirendai.com");
            //__jsl_clearance.Expires = dt;
            //var __jsluid = new Cookie("__jsluid", ck, "/", "www.huirendai.com");

            //_task.Client.Cookies.Add(__jsluid);
            //_task.Client.Cookies.Add(__jsl_clearance);

            //foreach (Cookie o in _task.Client.Cookies.GetCookies(new Uri("http://www.huirendai.com")))
            //{
            //    logger.Info(o.Name + " : " + o.Value);
            //}

            try
            {
                html = task.Client.Get(post, headers);
            }
            catch (Exception)
            {
                html = task.Client.Get(post, headers);
            }

            var data = new {
                keywords = task.Uid,
                password = task.Pwd,
                valicode = "",
                logintype = "user"
            }.ToDictionary();

            var result1 = task.Client.Post(post, data, CreateHeaders(post));
            var result = task.Client.Get("http://www.huirendai.com/index.php?user");
            if (!result.Contains("您的账户总资产"))
            {
                logger.Error("登陆失败");
                return false;
            }
            logger.Success("登陆成功");
            var sign = "http://www.huirendai.com/index.php?aj&q=user/sign";

            var result2 = task.Client.Post(sign, new { }.ToDictionary(), CreateHeaders("http://www.huirendai.com/index.php?user", isAjax: true));
            var json = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(result2);
            logger.Info(result2);
            var cd = (string)json.code;
            var msg = (string)json.msg;
            if (cd == "00000")
            {
                logger.Info(msg);
            }
            else
            {
                logger.Error(msg);
            }
            var l = "http://www.huirendai.com/index.php?activity&q=award";
            var luck = task.Client.Get(l);
            var id = Regex.Match(luck, @"user_id = '(\d+)'").Get(1);
            logger.Info("用户ID：" + id);


            while (true)
            {
                var r = task.Client.Post(l, new
                {
                    func = "lucky",
                    user_id = id,
                    activity = "ZNQ"
                }.ToDictionary(), CreateHeaders(l, isAjax: true));
                var json2 = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(r);
                if ((string)json2.code != "000")
                {
                    logger.Error("无抽奖机会");
                    return false;
                }

                var dicts = new Dictionary<string, string> { 
                { "1","10元现金卷" },
                { "2","下次再来" },
                { "3","IPhone6" },
                { "4","50惠米" },
                { "5","500京东卡" },
                { "6","100京东卡" },
                { "7","Watch!" },
                { "8","再来一次" }
            };
                var pid = (int)json2.data.prize_id;
                var pname = dicts[pid.ToString()];
                if (pid > 2 && pid < 8)
                {
                    logger.Success(pname);
                }
                else
                {
                    logger.Info(pname);
                }
                if (pid != 8) break;
            }
            
            return true;
        }
    }
}
