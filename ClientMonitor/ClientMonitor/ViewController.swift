//
//  ViewController.swift
//  ClientMonitor
//
//  Created by Daniel Barbosa on 24/06/23.
//

import UIKit
import RMQClient

class ViewController: UIViewController {

    @IBOutlet weak var tableView: UITableView!
    
    var messages = [String]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        tableView.dataSource = self
        
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: "DefaultCell")

        workerNamed("task_queue")
    }

    func createAlert() {
        let alert = UIAlertController(title: "Input Username", message: "type bellow your user name to be used in the chat", preferredStyle: UIAlertController.Style.alert)
        alert.addTextField()
        alert.addAction(UIAlertAction(title: "Confirm", style: UIAlertAction.Style.default, handler: { _ in
            let word = alert.textFields?.first?.text ?? "word"
            SocketIOManager.sharedInstance.addWatchedWord(word: word)
        }))
        self.present(alert, animated: true, completion: nil)
    }

    @IBAction func addWatchWord(_ sender: Any) {
        createAlert()
    }

    func workerNamed(_ name: String) {
        let conn = RMQConnection(delegate: RMQConnectionDelegateLogger())
        conn.start()
        let ch = conn.createChannel()
        let q = ch.queue("task_queue", options: .durable)
        ch.basicQos(1, global: false)
        print("\(name): Waiting for messages")
        let manualAck = RMQBasicConsumeOptions()
        q.subscribe(manualAck, handler: {(_ message: RMQMessage) -> Void in
            let messageText = String(data: message.body, encoding: .utf8) ?? ""
            self.messages.append(messageText)
            let sleepTime = UInt(messageText.components(separatedBy: ".").count) - 1
            DispatchQueue.main.async {
                self.tableView.reloadData()
            }
            ch.ack(message.deliveryTag)
        })
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
