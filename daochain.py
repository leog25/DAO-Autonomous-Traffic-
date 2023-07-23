import hashlib
import json
import time
import datetime as date


class Block:
    def __init__(self, data):
        self.timestamp = date.datetime.now()
        self.data = data
        self.previous_hash = None
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()
    
    def view_block(self):
        print([self.previous_hash, self.data, self.hash])

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]
    
    def get_chain(self):
        return self.chain

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
nex = Blockchain()

# class Transaction:
#     def __init__(self, sender, recipient, amount):
#         self.sender = sender
#         self.recipient = recipient
#         self.amount = amount

class Proposal:
    def __init__(self, owner, location):
        self.owner = owner
        self.location = location
        self.vote_location = []
        self.votes = {}

    def vote(self, member, vote):
        self.votes[member] = vote

    def is_approved(self):
        vote_sum = [0,0]
        for coordinate_1, coordinate_2 in self.votes.values():
            vote_sum[0] += coordinate_1
            vote_sum[1] += coordinate_2
        self.vote_location = [vote_sum[0]/ len(self.votes), vote_sum[1]/len(self.votes)]  #needs work implementing weaving out outliers, but will work for demo
        if self.vote_location == self.location:
            return True
        else: 
            return False

    

        # total_votes = sum(self.votes.values())
        # if total_votes > len(self.votes) / 2:
        #     return True
        # else:
        #     return False

class DAO:
    def __init__(self):
        self.members = {}
        self.proposals = []

    def add_member(self, address, stake):
        self.members[address] = stake

    def remove_member(self, address):
        self.members.pop(address)

    def create_proposal(self, owner, location):
        proposal = Proposal(owner, location)
        self.proposals.append(proposal)

    def vote_on_proposal(self, proposal, member, vote):  #vote = [49.00123, -73.000123] (coordinate data)
        proposal.vote(member, vote)

    def execute_proposal(self, proposal):
        if proposal.is_approved():
            nex.add_block(Block(proposal.vote_location))


            # for member, amount in proposal.votes.items():
            #     self.members[member] -= amount
            #     proposal.amount -= amount
            # Do something with the proposal funds

    def get_member_stake(self, member):
        return self.members[member]

    def get_total_stake(self):
        return sum(self.members.values())

    def get_proposals(self):
        return self.proposals
    
d = DAO()
d.add_member('a', 100)
d.add_member('b', 100)
d.add_member('c', 100)
d.create_proposal('object', [1.2323, 1.2343])
d.vote_on_proposal(d.proposals[0], 'a', [1.2323, 1.2343])
d.vote_on_proposal(d.proposals[0], 'b', [1.2323, 1.2343])
d.vote_on_proposal(d.proposals[0], 'c', [1.2323, 1.2343])
d.execute_proposal(d.proposals[0])

for o in nex.get_chain():
    o.view_block()







# The Transaction class represents a transaction in the DAO. It contains the sender's address, the recipient's address, and the amount transferred.

# The Proposal class represents a proposal in the DAO. It contains the proposer's address, a description of the proposal, the amount of tokens to be transferred if the proposal is approved, and a dictionary of votes. The calculate_hash method calculates the SHA-256 hash of the proposal.

# The DAO class represents the DAO itself. It contains a list of proposals, a dictionary of members with their addresses and token balances, the minimum quorum required for a proposal to pass, and the vote period in seconds.

# The add_member and remove_member methods add and remove members from the DAO.

# The add_proposal method adds a new proposal to the DAO.

# The vote method allows members to vote on a proposal. It takes the hash of the proposal, the voter's address, and the vote (True for yes, False for no).

# The execute_proposals method checks if each proposal has enough votes to pass. If it does, it calculates the number of yes and no votes, and if yes votes are greater than no votes, it transfers the requested tokens to the proposer's account.