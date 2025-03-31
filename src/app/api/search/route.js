export default async function POST(res) {
  
    const { query } = req.body;
    
    if (!query) {
      return res.status(400).json({ message: 'Query is required' });
    }

    return res.status(200).json({ message: 'Query received', query });
}