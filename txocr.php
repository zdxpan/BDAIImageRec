<?php
/**
 * User: zhoudaoxian
 * Date: 20190120
 * Time: 下午4:35
 * 应用名称测试
 * APPID2111435318 APPKEYizx4fOqgtab2BGq1 创建时间2019-01-18 22:18
 * 应用类型生活O2O  应用平台Android 应用描述哈哈哈哈
 */

// getReqSign ：根据 接口请求参数 和 应用密钥 计算 请求签名
function getReqSign($params /* 关联数组 */, $appkey /* 字符串*/)
{    
    ksort($params);  // 1. 字典升序排序

    $str = '';   // 2. 拼按URL键值对
    foreach ($params as $key => $value)
    {
        if ($value !== '')
        {
            $str .= $key . '=' . urlencode($value) . '&';
        }
    }    
    $str .= 'app_key=' . $appkey;    // 3. 拼接app_key
    
    $sign = strtoupper(md5($str));   // 4. MD5运算+转换大写，得到请求签名
    return $sign;
}
// doHttpPost ：执行POST请求，并取回响应结果
//   - $url   ：接口请求地址
//   - $params：完整接口请求参数（特别注意：不同的接口，参数对一般不一样，请以具体接口要求为准）
function doHttpPost($url, $params)
{
    $curl = curl_init();

    $response = false;
    do
    {
        // 1. 设置HTTP URL (API地址)
        curl_setopt($curl, CURLOPT_URL, $url);

        // 2. 设置HTTP HEADER (表单POST)
        $head = array(
            'Content-Type: application/x-www-form-urlencoded'
        );
        curl_setopt($curl, CURLOPT_HTTPHEADER, $head);

        // 3. 设置HTTP BODY (URL键值对)
        $body = http_build_query($params);
        curl_setopt($curl, CURLOPT_POST, true);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $body);

        // 4. 调用API，获取响应结果
        curl_setopt($curl, CURLOPT_HEADER, false);
        curl_setopt($curl, CURLOPT_NOBODY, false);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, true);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        $response = curl_exec($curl);
        if ($response === false)
        {
            $response = false;
            break;
        }

        $code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        if ($code != 200)
        {
            $response = false;
            break;
        }
    } while (0);

    curl_close($curl);
    return $response;
}

// 应用密钥  腾讯
$appkey = 'izx4fOqgtab2BGq1';  #izx4fOqgtab2BGq1

echo "-------------------------图片OCR识别接口--------------------------------";
// 图片base64编码
$path   = '/Users/zhoudaoxian/Desktop/13910139906.jpg';
// $path = "/Users/zhoudaoxian/Documents/frame/沈13810387085.jpg";  # 图片太大，无法处理
// $path   = '/Users/zhoudaoxian/Desktop/testbig.jpg';
$data   = file_get_contents($path);
$base64 = base64_encode($data);
$params = array(
    'app_id'     => '2111435318',
    'image'      => $base64,
    'time_stamp' => strval(time()),
    'nonce_str'  => strval(rand()),
    'sign'       => '' #  待计算=-=-=-=
);
$params['sign'] = getReqSign($params, $appkey);
var_dump($params);
// 执行API调用

$url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_handwritingocr';
$response = doHttpPost($url, $params);
// $response2 = doHttpPost($jdurl, $jdparams);
echo $response;
// echo $response2


?>