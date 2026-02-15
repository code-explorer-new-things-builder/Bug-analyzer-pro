// Sample Java Code with Multiple Bugs for Testing
// Copy and paste this into the web app to test the code review assistant

import java.util.*;
import java.io.*;

public class BankingSystem {
    
    // Bug 1: Infinite loop without break condition
    public static void processTransactions(List<Transaction> transactions) {
        int i = 0;
        while (true) {
            System.out.println("Processing transaction: " + transactions.get(i).getId());
            i++;
        }
    }
    
    // Bug 2: Null pointer dereference
    public static double calculateBalance(Account account) {
        double balance = 0;
        for (Transaction t : account.getTransactions()) {
            balance += t.getAmount();
        }
        return balance;
    }
    
    // Bug 3: Unreachable code after return
    public static String validatePassword(String password) {
        if (password == null || password.length() < 8) {
            return "Invalid password";
        }
        return "Valid password";
        System.out.println("Password validation complete");  // Unreachable
    }
    
    // Bug 4: Off-by-one error in loop
    public static void printAccountNumbers(String[] accounts) {
        for (int i = 0; i <= accounts.length; i++) {
            System.out.println("Account: " + accounts[i]);  // ArrayIndexOutOfBoundsException
        }
    }
    
    // Bug 5: Hardcoded credentials
    public static boolean authenticate(String username, String password) {
        String adminPassword = "admin123";  // Security issue
        String apiKey = "sk-1234567890abcdef";  // Hardcoded API key
        
        if (username.equals("admin") && password.equals(adminPassword)) {
            return true;
        }
        return false;
    }
    
    // Bug 6: SQL injection vulnerability (simulated)
    public static String buildQuery(String userId) {
        String query = "SELECT * FROM users WHERE id = " + userId;  // Unsafe concatenation
        return query;
    }
    
    // Bug 7: Missing null check
    public static int getTransactionCount(Account account) {
        return account.getTransactions().size();  // account could be null
    }
    
    // Bug 8: Infinite recursion without base case
    public static int calculateFactorial(int n) {
        return n * calculateFactorial(n - 1);  // No base case
    }
    
    // Bug 9: Logic error - comparison mistake
    public static boolean isValidAmount(double amount) {
        if (amount > 0 && amount < 1000000) {
            return true;
        }
        if (amount == 0) {
            return true;  // Zero amount should be invalid
        }
        return false;
    }
    
    // Bug 10: Resource leak - file not closed
    public static String readTransactionLog(String filename) throws IOException {
        FileReader fr = new FileReader(filename);
        BufferedReader br = new BufferedReader(fr);
        String line = br.readLine();
        return line;
        // fr and br never closed - resource leak
    }
}

// Bug 11: Missing null check in constructor
class Account {
    private String accountNumber;
    private double balance;
    private List<Transaction> transactions;
    
    public Account(String accountNumber, List<Transaction> transactions) {
        this.accountNumber = accountNumber;
        this.transactions = transactions;
        this.balance = calculateInitialBalance();
    }
    
    // Bug 12: Null pointer in method
    private double calculateInitialBalance() {
        double total = 0;
        for (Transaction t : transactions) {  // transactions could be null
            total += t.getAmount();
        }
        return total;
    }
    
    public List<Transaction> getTransactions() {
        return transactions;
    }
    
    // Bug 13: Unreachable code
    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        balance += amount;
        System.out.println("Deposit successful");
        return;
        System.out.println("This line is unreachable");  // Dead code
    }
    
    // Bug 14: Missing validation
    public void withdraw(double amount) {
        balance -= amount;  // No check if balance is sufficient
        System.out.println("Withdrawal of " + amount + " completed");
    }
}

// Bug 15: Infinite loop in constructor
class Transaction {
    private String id;
    private double amount;
    private String type;
    
    public Transaction(String id, double amount, String type) {
        this.id = id;
        this.amount = amount;
        this.type = type;
        
        // Bug 16: Infinite loop
        int counter = 0;
        while (counter < 10) {
            System.out.println("Initializing transaction...");
            // counter never incremented - infinite loop
        }
    }
    
    public String getId() {
        return id;
    }
    
    public double getAmount() {
        return amount;
    }
    
    // Bug 17: Logic error - wrong comparison
    public boolean isDebit() {
        if (type == "DEBIT") {  // Should use .equals()
            return true;
        }
        return false;
    }
    
    // Bug 18: Unreachable code after exception
    public void processTransaction() {
        try {
            if (amount < 0) {
                throw new Exception("Invalid amount");
            }
            System.out.println("Transaction processed");
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
            return;
            System.out.println("This is unreachable");  // Dead code
        }
    }
}

// Bug 19: Missing null check in loop
class TransactionProcessor {
    public static void processAllTransactions(List<Account> accounts) {
        for (Account account : accounts) {
            List<Transaction> transactions = account.getTransactions();
            for (Transaction t : transactions) {  // transactions could be null
                System.out.println("Processing: " + t.getId());
            }
        }
    }
    
    // Bug 20: Off-by-one error
    public static void printTransactions(Transaction[] transactions) {
        for (int i = 0; i <= transactions.length; i++) {  // Should be <, not <=
            System.out.println(transactions[i].getId());
        }
    }
    
    // Bug 21: Recursive call without proper base case
    public static int sumTransactionAmounts(List<Transaction> transactions, int index) {
        if (index == transactions.size()) {
            return 0;
        }
        return (int) transactions.get(index).getAmount() + 
               sumTransactionAmounts(transactions, index + 1);  // Could cause stack overflow
    }
}

// Bug 22: Missing null check
class ReportGenerator {
    public static void generateReport(Account account) {
        System.out.println("Account: " + account.getAccountNumber());  // account could be null
        System.out.println("Balance: " + account.getBalance());
        System.out.println("Transactions: " + account.getTransactions().size());
    }
    
    // Bug 23: Hardcoded values
    public static String formatCurrency(double amount) {
        String currency = "USD";  // Hardcoded
        String locale = "en_US";  // Hardcoded
        return currency + " " + String.format("%.2f", amount);
    }
}
