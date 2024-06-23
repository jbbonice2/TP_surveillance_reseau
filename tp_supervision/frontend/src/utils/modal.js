import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import { CKEditor } from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import axios from 'axios';

const AddArticleModal = ({ show, handleClose }) => {
    const [title, setTitle] = useState('');
    const [tag, setTag] = useState('');
    const [category, setCategory] = useState('');
    const [description, setDescription] = useState('');

    const [image, setImage] = useState(null);



    const handleEditorChange = (event, editor) => {
        const data = editor.getData();
        setDescription(data);};


 const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const user = JSON.parse(localStorage.getItem('user'));
            const formData = new FormData();
            formData.append('title', title);
            formData.append('content', description);
            formData.append('tag', tag);
            formData.append('category', category);
            formData.append('description', description);
            formData.append('image', image);
            formData.append('user', user.username);


            await axios.post('http://localhost:8000/articles/create/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then((res)=>{
                console.log(res);
                if(res.data.error){
                    alert(res.data.error);
                }
                else{
                    alert(res.data.message);
                }
            }).catch((errors)=>{
                console.log(errors);
            })

            // Réinitialiser le formulaire après la soumission réussie
            setTitle('');
            setTag('');
            setCategory('');
            setDescription('');
            setImage(null);
        } catch (error) {
            console.error('Error submitting article:', error);
        }
    };

    const handleImageChange = (event) => {
        setImage(event.target.files[0]);
    };
    

    return (
        <Modal show={show} style={{with:'90%'}}onHide={handleClose} >
            <Modal.Header closeButton>
                <Modal.Title>Add Article</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form className='col-lg-12 container'>
                    <Form.Group  className= 'form-group ' controlId="formTitle">
                        <Form.Label className='form-label'>Title</Form.Label>
                        <Form.Control type="text" placeholder="Enter title" value={title} onChange={(e) => setTitle(e.target.value)} />
                    </Form.Group>
                    <Form.Group className='form-group' controlId="formTag">
                        <Form.Label className='form-label'>Tag</Form.Label>
                        <Form.Control className='form-control' type="text" placeholder="Enter tag" value={tag} onChange={(e) => setTag(e.target.value)} />
                    </Form.Group>
                    <Form.Group className='form-group' controlId="formCategory">
                        <Form.Label className='form-label' >Category</Form.Label>
                        <Form.Control className='form-control' type="text" placeholder="Enter category" value={category} onChange={(e) => setCategory(e.target.value)} />
                    </Form.Group>
                    <Form.Group className='form-group' controlId="formDescription">
                        <Form.Label className='form-label'>Description</Form.Label>
                        <CKEditor
                        editor={ ClassicEditor }
                            data={description}
                            onBlur={handleEditorChange}
                        />
                    </Form.Group>
                    <Form.Group  className='form-group' controlId="formImage">
                        <Form.Label className='form-label' >Image</Form.Label>
                        <Form.Control   className='form-control' type="file" onChange={handleImageChange} />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Close
                </Button>
                <Button variant="success" onClick={handleSubmit}>
                    Save
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default AddArticleModal;
