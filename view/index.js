const playerStatus = document.querySelector('.game-status')

const valuePlayer1 = document.querySelector('.value-player')
const valuePlayer2 = document.querySelector('.value-computer')
const valueTied = document.querySelector('.value-tied')

const percentagePlayer1 = document.querySelector('.percentage-value-player')
const percentagePlayer2 = document.querySelector('.percentage-value-computer')
const percentageTied = document.querySelector('.percentage-value-tied')

const player1 = 'X'
const player2 = 'O'

let player1Points = 0
let player2Points = 0
let tiedPoints = 0

const initialState = [['', '', ''], ['', '', ''], ['', '', '']]
const copy = state => state.map(inner => inner.slice())
let gameState = copy(initialState)
let currentPlayer = player1

const toggleModal = () => {
    const modalElement = document.querySelector('.modal')
    modalElement.classList.toggle('hidden')
}

const toggleRestartButton = () => {
    playerStatus.classList.add('hidden')
    const buttonElement = document.querySelector('#restart')
    buttonElement.classList.toggle('hidden')
}

const applyPorcentage = () => {
    let totalGame = player1Points + player2Points + tiedPoints
    percentagePlayer1.innerHTML = ((100 * player1Points) / totalGame).toFixed(2) + "%"
    percentagePlayer2.innerHTML = ((100 * player2Points) / totalGame).toFixed(2) + "%"
    percentageTied.innerHTML = ((100 * tiedPoints) / totalGame).toFixed(2) + "%"
}

const applyPoints = (symbol) => {
    if (symbol === player1) {
        player1Points += 1
        valuePlayer1.innerHTML = player1Points
    } else if (symbol === player2) {
        player2Points += 1
        valuePlayer2.innerHTML = player2Points
    } else {
        tiedPoints += 1
        valueTied.innerHTML = tiedPoints
    }
    applyPorcentage()
}

const handleIconByCurrentPlayer = (currentPlayer) => {
    return currentPlayer === 'X' ? '<i class="fas fa-times" aria-hidden="true"></i>' : '<i class="far fa-circle" aria-hidden="true"></i>'  
}

const handleCellPlayed = (x, y) => {
    gameState[x][y] = currentPlayer;
    const clickedCell = document.querySelector(`[data-cell-index="${x} ${y}"]`)
    clickedCell.innerHTML = handleIconByCurrentPlayer(currentPlayer);
    currentPlayer = currentPlayer === player1 ? player2 : player1
}

const handleCellClick = (websocket) => (clickedCellEvent) => {
    const clickedCell = clickedCellEvent.target;
    const [x, y] = clickedCell.getAttribute('data-cell-index')
        .split(' ')
        .map(index => parseInt(index));

    if (gameState[x][y] !== "") {
        return;
    }

    websocket.send(JSON.stringify({ x, y }))
    handleCellPlayed(x, y);
}

const handleStartClick = (websocket) => (clickedStartEvent) => {
    const option = document.querySelector('input[name="menu-option"]:checked').value;
    const algorithm = document.querySelector('#menu-algorithm').value;
    websocket.send(JSON.stringify({ algorithm: parseInt(algorithm), option: parseInt(option) }))
    toggleModal()
}

const resetGame = (websocket) => {
    document.querySelectorAll('.cell').forEach(cell => cell.innerHTML = '')
}

const handleRestartClick = (websocket) => (clickedRestartEvent) => {
    resetGame(websocket)
    gameState = copy(initialState)
    currentPlayer = player1
    websocket.send({ type: 'RESTART' })
    toggleRestartButton()
}

window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:8765/");

    document.querySelectorAll('.cell').forEach(cell => cell.addEventListener('click', handleCellClick(websocket)));
    document.querySelector('#start').addEventListener('click', handleStartClick(websocket));
    document.querySelector('#restart').addEventListener('click', handleRestartClick(websocket));

    websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
        case 'MENU':
        toggleModal()
        break
        case 'MOVEMENT':
        handleCellPlayed(parseInt(event.x), parseInt(event.y))
        break
        case 'WINNER':
        const { player } = event
        if (player !== '') {
            applyPoints(player)
            playerStatus.innerHTML = `Player ${player} win!`
            playerStatus.classList.remove('hidden')
        } else {
            applyPoints('tie')
            playerStatus.innerHTML = `Is a tie :(`
            playerStatus.classList.remove('hidden')
        }
        setTimeout(() => {
            toggleRestartButton()
        }, 1000)
        break
    }
    })
});