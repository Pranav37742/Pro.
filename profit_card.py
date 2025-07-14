import tkinter as tk
from tkinter import messagebox

def calculate_profit():
    try:
        cp = float(entry_cp.get())
        sp = float(entry_sp.get())
        qty = int(entry_qty.get())

        total_cp = cp * qty
        total_sp = sp * qty
        profit = total_sp - total_cp

        result_text = f"""
        -------- PROFIT CARD --------
        Cost Price (each): ₹{cp:.2f}
        Selling Price (each): ₹{sp:.2f}
        Quantity: {qty}
        ------------------------------
        Total Cost Price: ₹{total_cp:.2f}
        Total Selling Price: ₹{total_sp:.2f}
        ------------------------------
        {'Profit' if profit > 0 else 'Loss' if profit < 0 else 'No Profit No Loss'}: ₹{abs(profit):.2f}
        """

        text_result.config(state='normal')
        text_result.delete(1.0, tk.END)
        text_result.insert(tk.END, result_text)
        text_result.config(state='disabled')

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Serve the HTML frontend (you can save your HTML as a separate file and render_template)
HTML_PAGE = """ 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Profit Card Generator - Flask</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
<body>
  <h2>Profit Card Generator (Python Flask Backend)</h2>
  <form id="profitForm">
    <label>Cost Price:</label><br />
    <input type="number" id="cp" name="cp" required step="0.01" /><br />
    <label>Selling Price:</label><br />
    <input type="number" id="sp" name="sp" required step="0.01" /><br />
    <label>Quantity:</label><br />
    <input type="number" id="qty" name="qty" required /><br /><br />
    <button type="submit">Calculate Profit</button>
  </form>
  <pre id="result" style="margin-top:20px; background:#eee; padding:10px;"></pre>

  <script>
    const form = document.getElementById('profitForm');
    const result = document.getElementById('result');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const cp = parseFloat(form.cp.value);
      const sp = parseFloat(form.sp.value);
      const qty = parseInt(form.qty.value);

      const response = await fetch('/calculate', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({cp, sp, qty})
      });

      const data = await response.json();
      if (data.error) {
        result.textContent = "Error: " + data.error;
      } else {
        result.textContent = `
Cost Price (each): ₹${cp.toFixed(2)}
Selling Price (each): ₹${sp.toFixed(2)}
Quantity: ${qty}
---------------------------
Total Cost Price: ₹${data.total_cp.toFixed(2)}
Total Selling Price: ₹${data.total_sp.toFixed(2)}
---------------------------
${data.status}: ₹${data.profit.toFixed(2)}
        `;
      }
    });
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/calculate", methods=["POST"])
def calculate_profit():
    data = request.get_json()
    try:
        cp = float(data.get("cp", 0))
        sp = float(data.get("sp", 0))
        qty = int(data.get("qty", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input data"}), 400

    if qty <= 0:
        return jsonify({"error": "Quantity must be greater than zero"}), 400

    total_cp = cp * qty
    total_sp = sp * qty
    profit = total_sp - total_cp

    if profit > 0:
        status = "Profit"
    elif profit < 0:
        status = "Loss"
        profit = abs(profit)
    else:
        status = "No Profit No Loss"

    return jsonify({
        "total_cp": total_cp,
        "total_sp": total_sp,
        "profit": profit,
        "status": status
    })

if __name__ == "__main__":
    app.run(debug=True)
