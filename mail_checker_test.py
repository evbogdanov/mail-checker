import unittest

from mail_checker import check, ERR_RULE_1, ERR_RULE_2, ERR_RULE_3, \
                                ERR_RULE_4, ERR_RULE_5, ERR_RULE_6, \
                                ERR_RULE_7


class CheckTest(unittest.TestCase):

    def test_rule_1(self):
        self.assertIsNone(check('me@mail.com'))
        self.assertEqual(check('mail.com'), ERR_RULE_1)

    def test_rule_2(self):
        self.assertIsNone(check('me@com'))
        self.assertIsNone(check(f'me@{"c"*256}'))
        self.assertEqual(check('me@co'), ERR_RULE_2)
        self.assertEqual(check(f'me@{"c"*257}'), ERR_RULE_2)
        self.assertEqual(check('me@mail..com'), ERR_RULE_2)
        self.assertEqual(check('me@mail.,com'), ERR_RULE_2)

    def test_rule_3(self):
        self.assertIsNone(check('me@ma.il.com'))
        self.assertIsNone(check('me@_ma.il_.com'))
        self.assertEqual(check('me@-ma.il.com'), ERR_RULE_3)
        self.assertEqual(check('me@ma.il-.com'), ERR_RULE_3)

    def test_rule_4(self):
        self.assertIsNone(check(f'{"a"*128}@mail.com'))
        self.assertIsNone(check('abc.123_-@mail.com'))
        self.assertEqual(check(f'{"a"*129}@mail.com'), ERR_RULE_4)
        self.assertEqual(check('m~e@mail.com'), ERR_RULE_4)

    def test_rule_5(self):
        self.assertIsNone(check('m.e@mail.com'))
        self.assertIsNone(check('m.e.@mail.com'))
        self.assertEqual(check('m..e@mail.com'), ERR_RULE_5)

    def test_rule_6(self):
        self.assertIsNone(check('ev"bo"gd"an"ov@mail.com'))
        self.assertEqual(check('ev"@mail.com'), ERR_RULE_6)
        self.assertEqual(check('ev"bo"gd"anov@mail.com'), ERR_RULE_6)

    def test_rule_7(self):
        self.assertIsNone(check('evbo"!g,d:"anov@mail.com'))
        self.assertEqual(check('m!e@mail.com'), ERR_RULE_7)
        self.assertEqual(check('m,e@mail.com'), ERR_RULE_7)
        self.assertEqual(check('m:e@mail.com'), ERR_RULE_7)
        self.assertEqual(check('"ev!"bogd!anov@mail.com'), ERR_RULE_7)

if __name__ == '__main__':
    unittest.main()
