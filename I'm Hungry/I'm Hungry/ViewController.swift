import UIKit

struct Meal {
    let name: String
    let price: Double
    let hours: Range<Date>
    
    func isAvailable(at date: Date = Date()) -> Bool {
        return hours.contains(date)
    }
}

class ViewController: UIViewController {
    
    private var meals: [Meal] = [] {
        didSet {
            randomizeMeal()
        }
    }
    
    private let mealLabel: UILabel = {
        let label = UILabel()
        label.textAlignment = .center
        label.font = .systemFont(ofSize: 20)
        return label
    }()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemPink
        setupMealLabel()
        setupAddMealButton()
        setupRandomizeButton()
    }
    
    private func setupMealLabel() {
        view.addSubview(mealLabel)
        mealLabel.translatesAutoresizingMaskIntoConstraints = false
        mealLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor).isActive = true
        mealLabel.centerYAnchor.constraint(equalTo: view.centerYAnchor).isActive = true
    }
    
    private func setupAddMealButton() {
        let button = UIButton()
        button.setTitle("Add meal", for: .normal)
        button.addTarget(self, action: #selector(addMeal), for: .touchUpInside)
        view.addSubview(button)
        button.translatesAutoresizingMaskIntoConstraints = false
        button.centerXAnchor.constraint(equalTo: view.centerXAnchor).isActive = true
        button.bottomAnchor.constraint(equalTo: mealLabel.topAnchor, constant: -20).isActive = true
    }
    
    private func setupRandomizeButton() {
        let button = UIButton()
        button.setTitle("Randomize meal", for: .normal)
        button.addTarget(self, action: #selector(randomizeMeal), for: .touchUpInside)
        view.addSubview(button)
        button.translatesAutoresizingMaskIntoConstraints = false
        button.centerXAnchor.constraint(equalTo: view.centerXAnchor).isActive = true
        button.topAnchor.constraint(equalTo: mealLabel.bottomAnchor, constant: 20).isActive = true
    }
    
    @objc private func addMeal() {
        let alertController = UIAlertController(title: "Add Meal", message: "", preferredStyle: .alert)
        
        alertController.addTextField { textField in
            textField.placeholder = "Meal name"
        }
        
        alertController.addTextField { textField in
            textField.placeholder = "Meal price"
            textField.keyboardType = .decimalPad
        }
        
        alertController.addTextField { textField in
            textField.placeholder = "Available from (HH:mm)"
            textField.keyboardType = .numbersAndPunctuation
        }
        
        alertController.addTextField { textField in
            textField.placeholder = "Available until (HH:mm)"
            textField.keyboardType = .numbersAndPunctuation
        }
        
        let cancelAction = UIAlertAction(title: "Cancel", style: .cancel)
        
        let saveAction = UIAlertAction(title: "Save", style: .default) { _ in
            guard
                let name = alertController.textFields?[0].text, !name.isEmpty,
                let priceString = alertController.textFields?[1].text, let price = Double(priceString),
                let fromTimeString = alertController.textFields?[2].text, let fromTime = self.dateFromTimeString(fromTimeString),
                let untilTimeString = alertController.textFields?[3].text, let untilTime = self.dateFromTimeString(untilTimeString)
            else {
                // Handle error
                return
            }
            let meal = Meal(name: name, price: price, hours: fromTime..<untilTime)
            self.meals.append(meal)
        }
        
        alertController.addAction(cancelAction)
        alertController.addAction(saveAction)
        self.present(alertController, animated: true)
    }

    private func dateFromTimeString(_ timeString: String) -> Date? {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "HH:mm"
        return dateFormatter.date(from: timeString)
    }

    @objc private func randomizeMeal() {
        let availableMeals = meals.filter { $0.isAvailable() }
        if let randomMeal = availableMeals.randomElement() {
            mealLabel.text = "Meal: \(randomMeal.name), Price: \(randomMeal.price)"
        } else {
            mealLabel.text = "No meals available at this time."
        }
    }
}
