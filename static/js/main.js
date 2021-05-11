// const url = window.location.href
// const searchForm = document.getElementById('search-form')
// const searchInput = document.getElementById('search-input')
// const resultsBox = document.getElementById('result-card')

// const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

// const sendSearchData = (users) => {
//   $.ajax({
//     type: 'POST',
//     url: 'search/',
//     data: {
//       'csrfmiddlewaretoken': csrf,
//       'users': users
//     },
//     success: (res) => {
//       console.log(res)
//     },
//     error: (err) => {
//       console.log(err)
//     }
//   })
// }

// searchInput.addEventListener('keyup', (e) => {
//   console.log(e.target.value)

//   if(resultsBox.classList.contains('not-visible')) {
//     resultsBox.classList.remove('not-visible')
//   }

//   sendSearchData(e.target.value)
// })