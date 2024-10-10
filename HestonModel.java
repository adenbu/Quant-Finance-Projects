import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class HestonModel {
    private final double S0;
    private final double K;
    private final double T;
    private final double r;
    private final double kappa;
    private final double theta;
    private final double sigma;
    private final double rho;
    private final double v0;
    private final int nSimulations;
    private final int nSteps;

    public HestonModel(double S0, double K, double T, double r, double kappa, double theta, double sigma, double rho, double v0, int nSimulations, int nSteps) {
        this.S0 = S0;
        this.K = K;
        this.T = T;
        this.r = r;
        this.kappa = kappa;
        this.theta = theta;
        this.sigma = sigma;
        this.rho = rho;
        this.v0 = v0;
        this.nSimulations = nSimulations;
        this.nSteps = nSteps;
    }

    public List<List<Double>> generatePaths(boolean american) {
        double dt = T / nSteps;
        List<List<Double>> S = new ArrayList<>();
        List<List<Double>> v = new ArrayList<>();

        for (int t = 0; t <= nSteps; t++) {
            S.add(new ArrayList<>(nSimulations));
            v.add(new ArrayList<>(nSimulations));
            for (int i = 0; i < nSimulations; i++) {
                S.get(t).add(S0);
                v.get(t).add(v0);
            }
        }

        Random random = new Random();

        for (int t = 1; t <= nSteps; t++) {
            for (int i = 0; i < nSimulations; i++) {
                double W1 = random.nextGaussian();
                double W2 = rho * W1 + Math.sqrt(1 - rho * rho) * random.nextGaussian();

                double vt = Math.max(v.get(t - 1).get(i) + kappa * (theta - v.get(t - 1).get(i)) * dt + sigma * Math.sqrt(v.get(t - 1).get(i) * dt) * W2, 0.0);
                v.get(t).set(i, vt);

                double St = S.get(t - 1).get(i) * Math.exp((r - 0.5 * v.get(t - 1).get(i)) * dt + Math.sqrt(v.get(t - 1).get(i) * dt) * W1);
                S.get(t).set(i, St);
            }
        }

        return S;
    }

    public double optionPrice(String optionType, boolean american) {
        List<List<Double>> SPaths = generatePaths(american);
        List<Double> payoff = new ArrayList<>(nSimulations);

        for (int i = 0; i < nSimulations; i++) {
            double payoffValue;
            if (optionType.equalsIgnoreCase("call")) {
                payoffValue = Math.max(SPaths.get(nSteps).get(i) - K, 0.0);
            } else if (optionType.equalsIgnoreCase("put")) {
                payoffValue = Math.max(K - SPaths.get(nSteps).get(i), 0.0);
            } else {
                throw new IllegalArgumentException("Invalid option type. Choose 'call' or 'put'.");
            }
            payoff.add(payoffValue);
        }

        if (american) {
            for (int t = nSteps; t > 0; t--) {
                for (int i = 0; i < nSimulations; i++) {
                    double discountedPayoff = Math.exp(-r * (T / nSteps)) * payoff.get(i);
                    payoff.set(i, Math.max(payoff.get(i), discountedPayoff));
                }
            }
        } else {
            for (int i = 0; i < nSimulations; i++) {
                payoff.set(i, payoff.get(i) * Math.exp(-r * T));
            }
        }

        double sum = payoff.stream().mapToDouble(Double::doubleValue).sum();
        return sum / nSimulations;
    }

    public static void main(String[] args) {
        // Define initial parameters
        double S0 = 100.0;  // Initial stock price
        double K = 100.0;   // Strike price
        double T = 1.0;     // Time to maturity (in years)
        double r = 0.05;    // Risk-free interest rate
        double kappa = 2.0; // Speed of mean reversion
        double theta = 0.04; // Long-run variance
        double sigma = 0.3; // Volatility of variance
        double rho = -0.7;  // Correlation between asset returns and volatility
        double v0 = 0.04;   // Initial variance
        int nSimulations = 10000; // Number of simulations
        int nSteps = 100; // Number of time steps

        // Instantiate the Heston model
        HestonModel heston = new HestonModel(S0, K, T, r, kappa, theta, sigma, rho, v0, nSimulations, nSteps);

        // Price a European call option
        double callPrice = heston.optionPrice("call", false);
        System.out.println("European Call Option Price: " + callPrice);

        // Price an American call option
        double americanCallPrice = heston.optionPrice("call", true);
        System.out.println("American Call Option Price: " + americanCallPrice);
    }
}