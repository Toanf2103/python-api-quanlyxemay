import axios from 'axios';

const btn = document.getElementById('btn');
        btn.addEventListener('click',(e)=>{
            
            const stringList = ["chuỗi 1", "chuỗi 2", "chuỗi 3"];

            const listCar = {username:'1',password:'1'};

            // fetch('http://localhost:5000/login', {
            // method: 'POST',
            // headers: {
            //     'Content-Type': 'application/json',
            // },
            // body: JSON.stringify(listCar),
            // })
            // .then(response => response.json())
            // .then(data => {
            //     console.log('Response from API:', data);
            // })
            // .catch(error => {
            //     console.error('Error:', error);
            // });


            axios.post('http://localhost:5000/login', listCar)
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.error(error);
            });


        })