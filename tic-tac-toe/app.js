const status = document.querySelector('.status')
const block = document.querySelectorAll('.block')

const valuePlayer = document.querySelector('.value-player')
const valueComputer = document.querySelector('.value-computer')
const valueTied = document.querySelector('.value-tied')

const percentagePlayer = document.querySelector('.percentage-value-player')
const percentageComputer = document.querySelector('.percentage-value-computer')
const percentageTied = document.querySelector('.percentage-value-tied')

const game = document.querySelector(".game")
const modalElement = document.querySelector('.modal')

const blockAlignment = [
  [0, 1, 2],
  [0, 3, 6],
  [0, 4, 8],
  [1, 4, 7],
  [2, 5, 8],
  [2, 4, 6],
  [3, 4, 5],
  [6, 7, 8]
]

let computerPoints = 0
let playerPoints = 0
let tiedPoints = 0

let pause = false

let playerSymbol = ""
let computerSymbol = ""

function decideSymbol(symbol, secondSymbol) {
  return (
    playerSymbol = symbol,
    computerSymbol = secondSymbol,
    modalElement.classList.toggle('hidden'),
    status.innerHTML = `${symbol} é o próximo`
  )
}

function applyPorcentage() {
  let totalGame = computerPoints + playerPoints + tiedPoints

  percentagePlayer.innerHTML = ((100 * playerPoints) / totalGame).toFixed(2) + "%"
  percentageComputer.innerHTML = ((100 * computerPoints) / totalGame).toFixed(2) + "%"
  percentageTied.innerHTML = ((100 * tiedPoints) / totalGame).toFixed(2) + "%"
}

function applyPoints(symbol) {
  if (symbol === playerSymbol) {
    playerPoints += 1
    valuePlayer.innerHTML = playerPoints
  } else if (symbol === computerSymbol) {
    computerPoints += 1
    valueComputer.innerHTML = computerPoints
  } else {
    tiedPoints += 1
    valueTied.innerHTML = tiedPoints
  }
  applyPorcentage()
}

function gameStatus() {
  blockAlignment.forEach((item) => {
    const [firstBlock, secondBlock, thirdBlock] = item

    if (block[firstBlock].innerHTML && block[firstBlock].innerHTML === block[secondBlock].innerHTML && block[firstBlock].innerHTML === block[thirdBlock].innerHTML) {
      status.innerHTML = `${block[firstBlock].innerHTML} é o ganhador!`
      applyPoints(block[firstBlock].innerHTML)
      pause = true
    }
  })

  if (!pause && block[0].innerHTML && block[1].innerHTML && block[2].innerHTML && block[3].innerHTML && block[4].innerHTML && block[5].innerHTML && block[6].innerHTML && block[7].innerHTML && block[8].innerHTML) {
    status.innerHTML = 'O jogo empatou'
    applyPoints()
    pause = true
  }

  if (!pause) {
    status.innerHTML = `${status.innerHTML === playerSymbol + " é o próximo" ? computerSymbol : playerSymbol} é o próximo`
  }
}

function resetGame() {
  status.innerHTML = `${playerSymbol} é o próximo`
  block.forEach((item) => {
    item.innerHTML = ""
  })
  pause = false
}

function computerPlay() {
  if (!pause) {
    pause = true
    setTimeout(() => {
      blockAlignment.forEach((item) => {
        const [firstBlock, secondBlock, thirdBlock] = item

        if (pause && block[firstBlock].innerHTML && block[firstBlock].innerHTML === block[secondBlock].innerHTML && block[thirdBlock].innerHTML === "") {
          block[thirdBlock].innerHTML = computerSymbol
          pause = false
        }
      })

      if (pause) {
        const computerArray = Array.from(block).filter((item) => item.innerHTML === "")
        computerArray[Math.floor(Math.random() * computerArray.length)].innerHTML = computerSymbol
        pause = false
      }
      gameStatus()
    }, 1000)
  }
}

function userPlay() {
  game.addEventListener('click', (element) => {
    if (element.target.className === "block" && !pause && element.target.innerHTML === "") {
      element.target.innerHTML = playerSymbol
      gameStatus()
      computerPlay()
    }
  })
}
userPlay()


// var socket = new WebSocket("127.0.0.0:5050");
// socket.onopen = function () {
//     alert("alerting you");
//     socket.send('Pingel');
// };

