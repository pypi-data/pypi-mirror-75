#Copyright (c) 2020 Jan Kiefer
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

class ListCmd:
	
	def feed(self, utfmsg):
		pass
	def is_complete(self):
		return False
	def get_data(self):
		return None

class MayVote(ListCmd):
	
	def __init__(self, utfmsg):
		self.may_vote = utfmsg.get_boolean_arg(1)
		self.vote_count = utfmsg.get_int_arg(2)