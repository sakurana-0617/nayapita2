var url = location.href ;
console.log(url)
$(function(){
    var qrtext = url;
    console.log(qrtext);
    var utf8qrtext = unescape(encodeURIComponent(qrtext));
    $("#img-qr").html("");
    $("#img-qr").qrcode({text:utf8qrtext}); 
  });

// $(function(){
//   const imgs = ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg'];  // 画像ファイル名
//   let index = 0;  // インデックス番号

//   // 初期画像の表示
//   $('.img').attr('src', 'images/' + imgs[index]);
  
//   // ボタンクリックイベント
//   $('#changeBtn').click(function(){
//     // 最後の画像判定
//     if(index == imgs.length - 1){
//       index = 0;
//     }else{
//       index++;
//     }
//     // 画像の切り替え
//     $('.img').attr('src', 'images/' + imgs[index]);
//   });
// });

$(function(){
  $("#footer_img").click(function(){
      $(".azarashi").attr('src','https://pbs.twimg.com/profile_images/1038750844777246720/_9ad4igG_400x400.jpg');
      });
});