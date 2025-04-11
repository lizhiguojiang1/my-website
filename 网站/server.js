const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const app = express();
const port = 3000;

// 连接 MongoDB 数据库
mongoose.connect('mongodb://localhost:27017/userdb');

// 定义用户模型
const UserSchema = new mongoose.Schema({
    username: String,
    email: String,
    password: String
});
const User = mongoose.model('User', UserSchema);

// 使用 body-parser 中间件解析请求体
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// 注册路由
app.post('/register', async (req, res) => {
    const { username, email, password, confirmPassword } = req.body;

    // 验证密码是否一致
    if (password !== confirmPassword) {
        return res.status(400).json({ message: '密码不一致' });
    }

    try {
        // 检查用户名和邮箱是否已存在
        const existingUser = await User.findOne({ $or: [{ username }, { email }] });
        if (existingUser) {
            return res.status(400).json({ message: '用户名或邮箱已存在' });
        }

        // 加密密码
        const hashedPassword = await bcrypt.hash(password, 10);

        // 创建新用户
        const newUser = new User({ username, email, password: hashedPassword });
        await newUser.save();

        res.status(201).json({ message: '注册成功' });
    } catch (error) {
        res.status(500).json({ message: '注册失败', error: error.message });
    }
});

// 启动服务器
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});