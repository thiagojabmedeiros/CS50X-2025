import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Soma as ações por símbolo (compras positivas, vendas negativas) e ignora posições zeradas/negativas
    positions = db.execute(
        """
        SELECT symbol, SUM(shares) AS shares
        FROM transactions
        WHERE user_id = :uid
        GROUP BY symbol
        HAVING SUM(shares) > 0
        """,
        uid=user_id,
    )

    holdings = []
    stocks_total = 0.0

    for row in positions:
        symbol = row["symbol"]
        shares = row["shares"]

        quote = lookup(symbol)  # {'name': ..., 'price': ..., 'symbol': ...}
        # fallback defensivo caso o lookup falhe por algum motivo
        name = quote["name"] if quote else symbol
        price = float(quote["price"]) if quote else 0.0

        total = shares * price
        stocks_total += total

        holdings.append(
            {
                "symbol": symbol,
                "name": name,
                "shares": shares,
                "price": price,
                "total": total,
            }
        )

    # Saldo em caixa do usuário
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)[0]["cash"]
    grand_total = stocks_total + cash

    return render_template(
        "index.html",
        holdings=holdings,
        cash=cash,
        stocks_total=stocks_total,
        grand_total=grand_total,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    # --------- Coleta e validação dos campos ----------
    symbol = (request.form.get("symbol") or "").strip().upper()
    shares_raw = (request.form.get("shares") or "").strip()

    if not symbol:
        return apology("must provide symbol", 400)

    quote = lookup(symbol)
    if quote is None:
        return apology("invalid symbol", 400)

    try:
        shares = int(shares_raw)
    except (TypeError, ValueError):
        return apology("shares must be an integer", 400)

    if shares <= 0:
        return apology("shares must be positive", 400)

    price = quote["price"]
    cost = shares * price

    user_id = session["user_id"]
    rows = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
    if len(rows) != 1:
        return apology("user not found", 400)

    cash = rows[0]["cash"]
    if cost > cash:
        return apology("insufficient funds", 400)

    db.execute(
        "UPDATE users SET cash = cash - :cost WHERE id = :id",
        cost=cost, id=user_id
    )

    db.execute(
        """
        INSERT INTO transactions (user_id, symbol, shares, price)
        VALUES (:user_id, :symbol, :shares, :price)
        """,
        user_id=user_id,
        symbol=quote["symbol"],
        shares=shares,
        price=price
    )

    flash("Bought!")
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]

    # Busca todas as transações do usuário (compras e vendas)
    rows = db.execute(
        """
        SELECT symbol,
               shares,
               price,
               timestamp
        FROM transactions
        WHERE user_id = :uid
        ORDER BY timestamp DESC, id DESC
        """,
        uid=user_id
    )

    # Transforma os dados para facilitar a renderização
    # - type: "BUY" se shares > 0, "SELL" se shares < 0
    # - shares_abs: valor absoluto para exibir (ex.: vender 3 aparece como 3)
    history = []
    for r in rows:
        history.append({
            "symbol":     r["symbol"],
            "type":       "BUY" if r["shares"] > 0 else "SELL",
            "shares_abs": abs(int(r["shares"])),
            "price":      float(r["price"]),
            "when":       r["timestamp"],  # timestamp do banco
        })

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    symbol = (request.form.get("symbol") or "").strip().upper()
    if not symbol:
        return apology("must provide symbol", 400)

    quote_data = lookup(symbol)
    if quote_data is None:
        return apology("invalid symbol", 400)

    # aqui garantimos que o preço vai sair com DUAS casas decimais (ex: 28.00)
    price_str = f"{quote_data['price']:.2f}"

    return render_template("quoted.html",
                           symbol=quote_data["symbol"],
                           name=quote_data["name"],
                           price_str=price_str)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must give Username")
        if not password:
            return apology("Must give password")
        if not confirmation:
            return apology("Must give confirmation")

        if password != confirmation:
            return apology("Passwords do not match")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username already exists")

        session["user_id"] = new_user

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "GET":
        # Busca apenas símbolos com posição positiva para popular o <select>
        symbols = db.execute(
            """
            SELECT symbol, SUM(shares) AS shares
            FROM transactions
            WHERE user_id = :uid
            GROUP BY symbol
            HAVING SUM(shares) > 0
            """,
            uid=user_id,
        )
        return render_template("sell.html", symbols=symbols)

    # ---------- POST ----------
    symbol = (request.form.get("symbol") or "").strip().upper()
    shares_raw = (request.form.get("shares") or "").strip()

    # Validar símbolo selecionado
    if not symbol:
        return apology("must select a stock", 400)

    # Validar número de ações (inteiro positivo)
    try:
        shares_to_sell = int(shares_raw)
    except (TypeError, ValueError):
        return apology("shares must be an integer", 400)

    if shares_to_sell <= 0:
        return apology("shares must be positive", 400)

    # Conferir se o usuário possui ações suficientes desse símbolo
    pos = db.execute(
        """
        SELECT COALESCE(SUM(shares), 0) AS shares
        FROM transactions
        WHERE user_id = :uid AND symbol = :symbol
        """,
        uid=user_id, symbol=symbol
    )[0]["shares"]

    if pos <= 0:
        return apology("you don't own this stock", 400)

    if shares_to_sell > pos:
        return apology("too many shares", 400)

    # Buscar preço atual
    quote = lookup(symbol)
    if quote is None:
        return apology("invalid symbol", 400)

    price = float(quote["price"])
    proceeds = shares_to_sell * price

    # Creditar o caixa do usuário
    db.execute(
        "UPDATE users SET cash = cash + :amount WHERE id = :id",
        amount=proceeds, id=user_id
    )

    # Registrar a transação com shares NEGATIVOS
    db.execute(
        """
        INSERT INTO transactions (user_id, symbol, shares, price)
        VALUES (:user_id, :symbol, :shares, :price)
        """,
        user_id=user_id,
        symbol=quote["symbol"],  # normalizado pelo provider
        shares=-shares_to_sell,  # negativo para venda
        price=price
    )

    flash("Sold!")
    return redirect("/")
