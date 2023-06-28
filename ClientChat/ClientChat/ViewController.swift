//
//  ViewController.swift
//  ClientChat
//
//  Created by Daniel Barbosa on 24/06/23.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var tableView: UITableView!

    @IBOutlet weak var textField: UITextField!

    var messages = [String]()

    override func viewDidLoad() {
        super.viewDidLoad()

        tableView.dataSource = self
        
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: "DefaultCell")
        
        SocketIOManager.sharedInstance.listenForMessages { string in
            self.messages.append(string)
            self.tableView.reloadData()
        }
        
        createAlert()
    }

    func createAlert() {
        let alert = UIAlertController(title: "Input Username", message: "type bellow your user name to be used in the chat", preferredStyle: UIAlertController.Style.alert)
        alert.addTextField()
        alert.addAction(UIAlertAction(title: "Confirm", style: UIAlertAction.Style.default, handler: { _ in
            let username = alert.textFields?.first?.text ?? "username"
            SocketIOManager.sharedInstance.username = username
            self.title = username
            self.textField.becomeFirstResponder()
            SocketIOManager.sharedInstance.establishConnection()
        }))
        self.present(alert, animated: true, completion: nil)
    }

    @IBAction func didPressSend(_ sender: Any) {
        let message = "{\(SocketIOManager.sharedInstance.username)}: \(textField.text ?? "")"
        SocketIOManager.sharedInstance.sendMessage(message: message)
        textField.text = ""
    }
}

extension ViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return messages.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "DefaultCell")
        cell?.textLabel?.text = messages[indexPath.row]
        return cell ?? UITableViewCell()
    }
}
