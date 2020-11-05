document.addEventListener("DOMContentLoaded", main);

class API {
    constructor() {
        this.base_url = 'http://127.0.0.1/api';
    }

    async GETRequest(url) {
        return await fetch(this.base_url + url)
            .then(response => {
                return response.json()
            })
    }

    async POSTRequest(url, data) {
        return await fetch(this.base_url + url, {
            method: 'POST',
            headers: {
            'X-CSRFToken': document.cookie.match('csrftoken').input.slice(10),
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': window.location.host
            },
            body: JSON.stringify(data)
        }).then(response => {
            return response.json()
        })
    }
}

class OrdersContainer {
    constructor() {
        this.container = document.getElementsByClassName('dynamic-orderitem_set')
        this.breakfast = document.getElementById('orderitem_set-0')
        this.lunch = document.getElementById('orderitem_set-1')
        this.dinner = document.getElementById('orderitem_set-2')
    }

    get mealtime_type_select() {
        return {
            'breakfast': this.breakfast.getElementsByTagName('select')[0],
            'lunch': this.lunch.getElementsByTagName('select')[0],
            'dinner': this.dinner.getElementsByTagName('select')[0],
        }
    }

    get products_select() {
        let obj =  {
            mealtime_type_products_select: [
                this.breakfast.getElementsByTagName('select')[1],
                this.lunch.getElementsByTagName('select')[1],
                this.dinner.getElementsByTagName('select')[1]
            ],
            selected_options: [],

            add_new_options(data) {
                for (let i in this.mealtime_type_products_select) {
                    this.selected_options.push([])
                    let options = this.mealtime_type_products_select[i].options
                    for (let j = options.length - 1; options.length > 0; j--) {
                        let option = this.mealtime_type_products_select[i].options[j]
                        if (option.hasAttribute('selected')) {
                            this.selected_options[i].push(option.value)
                        }
                        option.remove()
                   }
                    let products = data[i]
                    for (let j in products) {
                        let option = document.createElement('option')
                        option.setAttribute('value', products[j]['id'])
                        if (this.selected_options[i].indexOf(String(products[j]['id'])) !== -1) {
                            option.selected = true
                        }
                        option.innerText = products[j]['name']
                        this.mealtime_type_products_select[i].append(option)
                    }
                }
            }
        };
        return obj
    }
}

function put_mealtime_types(breakfast, lunch, dinner) {
    breakfast.options[1].setAttribute("selected", "")
    lunch.options[2].setAttribute("selected", "")
    dinner.options[3].setAttribute("selected", "")
}

function reload_products_select(data) {
    api = new API()
    api.POSTRequest('/date_choice', {'date': data }).then(data => {
        const orders_container = new OrdersContainer()
        let products_select = orders_container.products_select
        products_select.add_new_options(data)
    })
}

function handle_date_input(event) {
    reload_products_select(event.target.value);
}



function main() {
    const orders_container = new OrdersContainer()
    const mealtime_types = orders_container.mealtime_type_select
    put_mealtime_types(mealtime_types['breakfast'], mealtime_types['lunch'], mealtime_types['dinner'])
    const date_input = document.getElementById('id_date')
    if (date_input.value) {
        reload_products_select(date_input.value)
    }
    date_input.addEventListener('input', handle_date_input)
}
