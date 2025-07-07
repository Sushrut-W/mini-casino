let playerList = [];
let currentPlayerIndex = 0;

function addPlayerInput() {
    const container = document.getElementById("player-inputs");
    const nameInput = document.createElement("input");
    nameInput.className = "pname";
    nameInput.placeholder = "Name";

    const depositInput = document.createElement("input");
    depositInput.className = "pdeposit";
    depositInput.placeholder = "Deposit";
    depositInput.type = "number";

    const betInput = document.createElement("input");
    betInput.className = "pbet";
    betInput.placeholder = "Bet";
    betInput.type = "number";

    container.appendChild(document.createElement("br"));
    container.appendChild(nameInput);
    container.appendChild(depositInput);
    container.appendChild(betInput);
}

function startGame() {
    document.getElementById("setup").style.display = "none";
    document.getElementById("play-again").style.display = "none";
    const names = document.getElementsByClassName("pname");
    const deposits = document.getElementsByClassName("pdeposit");
    const bets = document.getElementsByClassName("pbet");
    playerList = [];

    for (let i = 0; i < names.length; i++) {
    const name = names[i].value;
    const deposit = parseInt(deposits[i].value);
    const bet = parseInt(bets[i].value);
    if (name && !isNaN(deposit) && !isNaN(bet)) {
        playerList.push({ name: name, deposit: deposit, bet: bet });
    }
    }

    if (playerList.length === 0) {
    alert("Please enter at least one valid player.");
    return;
    }

    fetch("http://localhost:5000/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ players: playerList.map(p => ({ name: p.name, deposit: p.deposit })) })
    })
    .then(() => {
    Promise.all(playerList.map(p =>
        fetch("http://localhost:5000/bet", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: p.name, amount: p.bet })
        })
    )).then(() => {
        currentPlayerIndex = 0;
        render();
    });
    });
}

function sendAction(action) {
    const currentPlayer = playerList[currentPlayerIndex];
    fetch("http://localhost:5000/action", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: currentPlayer.name, action: action })
    })
    .then(() => {
    fetch("http://localhost:5000/state")
        .then(res => res.json())
        .then(data => {
        const player = data.players.find(p => p.name === currentPlayer.name);
        if (player.busted || player.standing) {
            currentPlayerIndex++;
        }
        render();

        if (currentPlayerIndex >= playerList.length) {
            const allDone = data.players.every(p => p.standing || p.busted);
            if (data.state !== "finished" && allDone) {
            fetch("http://localhost:5000/action", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: playerList[playerList.length - 1].name, action: "stand" })
            }).then(() => render());
            } else if (data.state === "finished") {
            document.getElementById("play-again").style.display = "inline-block";
            }
        }
        });
    });
}

function prepareNextRound() {
    document.getElementById("play-again").style.display = "none";
    document.getElementById("betting").style.display = "block";

    const betInputsDiv = document.getElementById("bet-inputs");
    betInputsDiv.innerHTML = "";

    playerList.forEach((p, i) => {
    const label = document.createElement("label");
    label.innerText = `${p.name}'s bet:`;
    const input = document.createElement("input");
    input.type = "number";
    input.value = p.bet;
    input.id = `bet-${i}`;
    betInputsDiv.appendChild(label);
    betInputsDiv.appendChild(input);
    betInputsDiv.appendChild(document.createElement("br"));
    });
}

function submitBets() {
    document.getElementById("betting").style.display = "none";
    currentPlayerIndex = 0;
    playerList.forEach((p, i) => {
    const newBet = parseInt(document.getElementById(`bet-${i}`).value);
    if (!isNaN(newBet)) p.bet = newBet;
    });

    fetch("http://localhost:5000/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ players: playerList.map(p => ({ name: p.name, deposit: p.balance })) })
    })
    .then(() => {
    Promise.all(playerList.map(p =>
        fetch("http://localhost:5000/bet", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: p.name, amount: p.bet })
        })
    )).then(() => render());
    });
}

function render() {
    fetch("http://localhost:5000/state")
    .then(res => res.json())
    .then(data => {
        document.getElementById("game").style.display = "block";

        const dealer = data.dealer;
        document.getElementById("dealer").innerHTML = `
        <strong>Dealer</strong><br>
        Hand: ${dealer.hand.join(", ")}<br>
        Score: ${dealer.score}
        `;

        const playersDiv = document.getElementById("players");
        playersDiv.innerHTML = "";

        data.players.forEach(p => {
        const playerEl = document.createElement("div");
        playerEl.className = "player";

        let status = "";
        if (data.state === "finished") {
            if (p.busted) status = '<span class="loss">BUSTED</span>';
            else if (p.blackjack) status = '<span class="blackjack">BLACKJACK!</span>';
            else if (p.score > dealer.score || dealer.busted) status = '<span class="win">WIN!</span>';
            else if (p.score < dealer.score) status = '<span class="loss">LOSS</span>';
            else status = '<span class="push">PUSH</span>';
        } else {
            if (p.blackjack) status = '<span class="blackjack">BLACKJACK!</span>';
            else if (p.busted) status = '<span class="loss">BUSTED</span>';
        }

        playerEl.innerHTML = `
            <strong>${p.name}</strong><br>
            Hand: ${p.hand.join(", ")}<br>
            Score: ${p.score}<br>
            Balance: $${p.balance}<br>
            Bet: $${p.bet}<br>
            ${status}
        `;
        playersDiv.appendChild(playerEl);
        });

        const currentName = playerList[currentPlayerIndex]?.name;
        document.getElementById("turn-indicator").innerText = currentName
        ? `Actions: ${currentName}'s turn`
        : "All players finished";

        if (data.state === "finished") {
        document.getElementById("play-again").style.display = "inline-block";
        playerList.forEach((p, i) => p.balance = data.players[i].balance);
        }
    });
}