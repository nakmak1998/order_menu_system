function create_slider_item(data) {
    let slider_container = document.createElement('div')
    slider_container.class = 'swiper-slide'
    let military = document.createElement('div')
    let military_img = document.createElement('img')
    let military_name = document.createElement('p')
    military_img.src = 'http://127.0.0.1/' + data.military.image
    military_name.textContent = data.military.name
    military.append(military_img)
    military.append(military_name)
    slider_container.append(military)
    data.products.map(product => {
        slider_container.append(document.createElement('p').text = product)
    })
    return slider_container
}

function startWebsocket() {
  var ws = new WebSocket( 'ws://' + window.location.host + '/ws/dist')


  ws.onmessage = function(e){
    console.log(e)
    let container = document.getElementById('slider')
    const data = JSON.parse(e.data)
    console.log('websocket message event:', data)
    let slider_item = document.createElement('div')
    slider_item = create_slider_item(data)
    container.append(slider_item)
  }

  ws.onclose = function(){
    // connection closed, discard old websocket and create a new one in 5s
    ws = null
    setTimeout(startWebsocket, 5000)
  }
}

startWebsocket();

var swiper = new Swiper('.swiper-container', {
      slidesPerView: 8,
      spaceBetween: 10,
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
    });