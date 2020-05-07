from nn import *
from dataset import *

net = Net()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

def train():
  net.train()
  for epoch in range(7):

    running_loss = 0.0
    for i, date in enumerate(trainloader, 0):
      inputs, labels = date
      optimizer.zero_grad()

      outputs = net(inputs)
      loss = criterion(outputs, labels)
      loss.backward()
      optimizer.step()

      running_loss += loss.item()
      if i % 2000 == 1999:
        print('[%d, %5d] loss: %.3f' %
                    (epoch + 1, i + 1, running_loss / 2000))
        running_loss = 0.0

  print("Finished Training")

  correct = 0
  total = 0
  with torch.no_grad():
    for date in testloader:
      images, labels = date
      outputs = net(images)
      _, predicted = torch.max(outputs, 1)
      total += labels.size(0)
      correct += (predicted == labels).sum().item()

  print('Accuracy of the network on the 10000 test images: %d %%' % (
      100 * correct / total))

  return net

